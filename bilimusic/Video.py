# pylint: disable=missing-module-docstring
import time

import requests

from .urlconvert import *
from .VideoPage import VideoPage


class Video:
    '''
    a video from bilibili
    '''

    def __init__(self, id_: str or int) -> None:

        if is_bvid(id_):
            self.bvid = id_
            self.url = bvid2url(self.bvid)
        elif is_av(id_):
            self.aid = id_
            self.url = av2url(self.aid)  # type: ignore
        elif is_url(id_):
            self.url = id_
            if url2bvid(self.url):
                self.bvid = url2bvid(self.url)
            elif url2av(self.url):
                self.aid = url2av(self.url)
            else:
                raise Exception("It's not a correct url to a bilibili video.")
        else:
            raise Exception(
                "It's not a bvid, av or url that can be used to link to a bilibili video.")
        self.pages = []

    def parse(self) -> None:
        r = requests.get(url='http://api.bilibili.com/x/web-interface/view',
                         params=dict(
                             bvid=self.bvid
                         ))
        data = r.json()['data']
        info = dict(
            audio_source_url=bvid2url(self.bvid),  # type: ignore
            title=data['title'],
            publisher=data['owner']['name'],
            publisher_url=mid2url(data['owner']['mid']),
            artist=data['owner']['name'],
            artist_url=mid2url(data['owner']['mid']),
            play_count=data['stat']['view'],
            release_date=time.strftime(
                '%Y-%m-%d', time.localtime(data['pubdate'])),
            copyright='自制' if data['copyright'] == 1 else '转载',
            imageurl=data['pic'],
        )
        info.update(dict(
            album=info['title'],
            album_artist=info['artist']
        ))
        # FIXME: 更加复杂的判断逻辑被加入
        for a in r.json()['data']['pages']:
            self.pages.append(
                VideoPage(self.bvid, a['cid'], info))  # type: ignore

    def __repr__(self) -> str:
        return f"Video(bvid={self.bvid},pages={','.join([f'VideoPage(cid={a.cid})' for a in self.pages])})"
