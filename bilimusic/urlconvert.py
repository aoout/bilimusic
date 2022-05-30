'''
provide judgment and conversion between av,bvid, url, and mid.
'''


from typing import Any, Optional


def is_bvid(text: str) -> bool:
    '''
    determine if this is a bvid
    '''
    return text.startswith('BV')


def is_av(text: Any) -> bool:
    '''
    determine if this is a av
    '''
    return isinstance(text, int)


def is_url(text: str) -> bool:
    '''
    determine if this is a url
    '''
    return text.startswith('https')


def bvid2url(bvid: str) -> str:
    '''
    convert a bvid to the url
    '''
    return f'https://www.bilibili.com/video/{bvid}'


def url2bvid(url: str) -> Optional[str]:
    '''
    convert a url to the bvid
    '''
    for i in url.split('/'):
        if i.startswith('BV'):
            return i.split('?')[0]
    return None


def av2url(av: int) -> Optional[str]:  # pylint: disable=invalid-name
    '''
    convert a av to the url
    '''
    return f'https://www.bilibili.com/video/av{av}'


def url2av(url: str) -> Optional[str]:
    '''
    convert a url to the av
    '''
    for i in url.split('/'):
        if i.startswith('av'):
            i = i.removeprefix('av')
            return i.split('?')[0]
    return None


def mid2url(mid: int) -> str:
    '''
    convert a bvid to the url
    '''
    return f"https://space.bilibili.com/{mid}"


# TODO:从av号形式的链接会进入链接中包含av号而不是bvid的链接。加入对于av号在api中的适配
