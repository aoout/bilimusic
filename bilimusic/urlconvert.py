'''
provide judgment and conversion between av,bvid, url, and mid.
'''


from typing import Any, Optional


def is_bvid(text: str) -> bool:
    '''
    determine if this is a bvid.
    but, the function can't ensure that it's a valid bvid.
    the purpose of the function is to identify bvid from av and url.
    '''
    return text.startswith('BV')


def is_av(text: Any) -> bool:
    '''
    determine if this is a av.
    but, the function can't ensure that it's a valid av.
    the purpose of the function is to identify av from bvid and url.
    '''
    return isinstance(text, int)


def is_url(text: str) -> bool:
    '''
    determine if this is a url.
    but, the function can't ensure that it's a valid url.
    the purpose of the function is to identify av from bvid and av.
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


def is_validurl(text: str) -> bool:
    '''
    determine if the text is a url that can be parsed out bvid or av.
    '''
    if is_url(text):
        if url2bvid(text) or url2av(text):
            return True
    return False


def mid2url(mid: int) -> str:
    '''
    convert a bvid to the url
    '''
    return f"https://space.bilibili.com/{mid}"


def is_what(text: Any) -> Optional[str]:
    '''
    determine what this is.
    '''
    if is_av(text):
        return 'av'
    if is_bvid(text):
        return 'bvid'
    if is_validurl(text):
        return 'url'
    return None


def extend_id(text: Any) -> Optional[dict]:
    '''
    obtain other identifiers from one identifier of the video.
    '''
    result = dict.fromkeys(['bvid', 'av', 'url'], None)
    type_ = is_what(text)
    if type_:
        if type_ == 'av':
            result.update(dict(av=text, url=av2url(text)))
        elif type_ == 'bvid':
            result.update(dict(bvid=text, url=bvid2url(text)))
        else:
            if url2bvid(text):
                result.update(dict(url=text, bvid=url2bvid(text)))
            else:
                result.update(dict(url=text, av=url2av(text)))
        return result
    return None