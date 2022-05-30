import time

import requests

from .urlconvert import *
from .VideoPage import VideoPage


class Video:
    def __init__(self, id_: str, lazyload: bool = False) -> None:

        self.bvid = id_ if is_bvid(id_) else url2bvid(id_)
        self.pages = list()
        if not lazyload:
            self.parse()

    def parse(self, correction: dict) -> None:
        r = requests.get(url='http://api.bilibili.com/x/web-interface/view',
                         params=dict(
                             bvid=self.bvid
                         ))
        data = r.json()['data']
        info = dict(
            audio_source_url=bvid2url(self.bvid),
            title=data['title'],
            publisher=data['owner']['name'],
            publisher_url=mid2url(data['owner']['mid']),
            artist=data['owner']['name'],
            artist_url=mid2url(data['owner']['mid']),
            play_count=data['stat']['view'],
            release_date=time.strftime(
                '%Y-%m-%d', time.localtime(data['pubdate'])),
            copyright='自制' if data['copyright'] == 1 else '转载',
            imageurl=data['pic']
        )
        info.update(dict(
            album=info['title'],
            album_artist=info['artist']
        ))
        info.update(correction)
        # FIXME: 更加复杂的判断逻辑被加入
        for a in r.json()['data']['pages']:
            self.pages.append(VideoPage(self.bvid, a['cid'], info))

    def __repr__(self) -> str:
        return f"Video(bvid={self.bvid},pages={','.join([f'VideoPage(cid={a.cid})' for a in self.pages])})"
