# pylint: disable=missing-module-docstring
from tempfile import NamedTemporaryFile

import eyed3
import requests
from moviepy.editor import AudioFileClip
from PIL import Image
from tqdm import tqdm

from .super_resolution import super_resolution
from .utils import square_jpeg


class VideoPage:
    def __init__(self, bvid: str, cid: str, info: dict) -> None:
        self.bvid = bvid
        self.cid = cid
        self.info = info

    def __repr__(self) -> str:
        return f'VideoPage(bvid={self.bvid},cid={self.cid})'

    def download(self, cleaner_cover: bool = False, cover_offset: float = 0.0) -> None:
        r = requests.get(url='http://api.bilibili.com/x/player/playurl',
                         params=dict(
                             bvid=self.bvid,
                             cid=self.cid,
                             fnval=16
                         ))
        url = r.json()['data']['dash']['audio'][0]['baseUrl']
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                   'referer': 'https://www.bilibili.com'}

        with NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            total = round(int(requests.head(
                url, headers=headers).headers['Content-Length']) / 1024 / 1024, 3)
            with requests.get(url, stream=True, headers=headers) as r:
                with tqdm(total=total, unit='mb') as pbar:
                    for chunk in r.iter_content(chunk_size=1024):
                        tmp.write(chunk)
                        pbar.update(round(len(chunk)/1024 / 1024, 3))
            AudioFileClip(tmp.name).write_audiofile(
                f"{self.info['title']}.mp3", bitrate='192k')

        self.attach_tag(cleaner_cover, cover_offset)

    def attach_tag(self, cleaner_cover: bool = False, cover_offset: float = 0.0) -> None:
        af = eyed3.load(f"{self.info['title']}.mp3")
        af.initTag(version=(2, 3, 0))
        for key, value in self.info.items():
            if key != "imageurl":
                setattr(af.tag, key, value)
            else:
                imagedata = requests.get(url=value).content
                imagedata = self.make_cover(
                    imagedata, cleaner_cover, cover_offset)
                af.tag.images.set(3, imagedata, "image/jpeg", u"cover")
                af.tag.save()

    def make_cover(self, imagedata: bytes, cleaner: bool = False, offset: float = 0.0) -> bytes:
        # TODO:解耦出一个将封面下载到本地的函数。并将其接口暴露给命令行解析。
        with NamedTemporaryFile(suffix='.jpg', delete=False) as tmp1, NamedTemporaryFile(suffix='.jpg', delete=False) as tmp2:
            tmp1.write(imagedata)
            if cleaner:
                super_resolution(tmp1.name, tmp1.name)
            img = Image.open(tmp1.name).convert('RGB')

            img = square_jpeg(img, offset)
            img.resize((500, 500))
            img.save(tmp2.name)
            return tmp2.read()
