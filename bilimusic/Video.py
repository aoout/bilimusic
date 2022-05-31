# pylint: disable=missing-module-docstring,no-member,access-member-before-definition,invalid-name,line-too-long
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
from moviepy.editor import AudioFileClip
from PIL import Image
from tqdm import tqdm

from .mp3 import Mp3
from .super_resolution import super_resolution
from .urlconvert import extend_id, mid2url
from .utils import bytes2md, square_jpeg


class Video:
    '''
    a video from bilibili
    '''

    def __init__(self, id_: str or int) -> None:
        if result := extend_id(id_):
            for key, value in result.items():
                setattr(self, key, value)
        else:
            raise Exception(
                "It's not a bvid, av or url that can be used to link to a bilibili video.")
        self._getinfo()

    def _getinfo(self) -> None:
        '''
        get the infomation about the video from bilibili.
        '''
        try:
            response = requests.get(url='http://api.bilibili.com/x/web-interface/view',
                                    params=dict(
                                        bvid=self.bvid
                                    ) if self.bvid else dict(
                                        aid=self.aid
                                    ))
            data = response.json()['data']
        except Exception as exception:
            raise Exception('some network porblems happended.') from exception

        if not self.av:
            self.av = data['aid']
        if not self.bvid:
            self.bvid = data['bvid']

        self.info = dict(
            title=data['title'],
            publisher=data['owner']['name'],
            publisher_url=mid2url(data['owner']['mid']),
            release_date=time.strftime(
                '%Y-%m-%d', time.localtime(data['pubdate'])),
            copyright='自制' if data['copyright'] == 1 else '转载'
        )
        self.imageurl = data['pic']

        self.cids = [a['cid'] for a in data['pages']]

    def _extendinfo_withguess(self) -> None:
        '''
        completing meta information by guessing
        '''
        self.info.update(dict(
            artist=self.info['publisher'],
            artist_url=self.info['publisher_url'],
            album=self.info['title'],
            album_artist=self.info['artist']
        ))

    def setinfo(self, info: dict) -> None:
        '''
        set info with  a dict.
        '''
        self.info.update(info)
        self._extendinfo_withguess()

    def __repr__(self) -> str:
        '''
        show the av, bvid, and the cids of its pages.
        '''
        return f"Video(av={self.av},bvid={self.bvid},cids={','.join(self.cids)})"

    def download_audio(self, page_index: int = 0, path: str or Path = None) -> None:
        '''
        download a page of the video.
        '''
        path = Path(path) if path else Path(f"{self.info['title']}.mp3")
        response = requests.get(url='http://api.bilibili.com/x/player/playurl',
                                params=dict(
                                    bvid=self.bvid,
                                    cid=self.cids[page_index],
                                    fnval=16
                                ))
        url = response.json()['data']['dash']['audio'][0]['baseUrl']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                   'referer': 'https://www.bilibili.com'}

        with NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            content_length = requests.head(
                url, headers=headers).headers['Content-Length']
            total = bytes2md(content_length)
            with requests.get(url, stream=True, headers=headers) as r:
                with tqdm(total=total, unit='mb') as pbar:
                    for chunk in r.iter_content(chunk_size=1024):
                        tmp.write(chunk)
                        pbar.update(bytes2md(len(chunk)))
            AudioFileClip(tmp.name).write_audiofile(path, bitrate='192k')

    def download_cover(self, path: str or Path = None) -> None:
        '''
        download the cover of the video.
        '''
        path = Path(path) if path else Path(f"{self.info['title']}.jpg")
        imagedata = requests.get(url=self.imageurl).content
        path.write_bytes(imagedata)

    def cut_cover(self, path: str or Path = None, offset: float = 0.0, size: tuple = (500, 500)) -> None:
        '''
        cut the cover to a square.
        '''
        path = Path(path) if path else Path(f"{self.info['title']}.jpg")
        img = Image.open(path).convert('RGB')
        img = square_jpeg(img, offset)
        img.resize(size)
        img.save(path)

    def clarify_cover(self, path: str or Path = None) -> None:
        '''
        make the cover more clean.
        '''
        path = Path(path) if path else Path(f"{self.info['title']}.jpg")
        super_resolution(path, path)

    def attach_tags(self, path: str or Path = None, cover_path: str or Path = None) -> None:
        '''
        attach tags to a mp3 file.
        '''
        path = Path(path) if path else Path(f"{self.info['title']}.mp3")
        cover_path = Path(cover_path) if path else Path(
            f"{self.info['title']}.jpg")
        mp3 = Mp3(path)
        mp3.initTag()
        mp3.settags_withdict(self.info)
        mp3.set_cover_fromfile(path)
