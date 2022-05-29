
def is_bvid(text: str) -> bool:
    return text.startswith('BV')


def is_url(text: str) -> bool:
    return text.startswith('https')


def bvid2url(bvid: str) -> str:
    return f'https://www.bilibili.com/video/{bvid}'


def url2bvid(url: str) -> str:
    for a in url.split('/'):
        if a.startswith('BV'):
            return a.split('?')[0]


def mid2url(mid: int) -> str:
    return f"https://space.bilibili.com/{mid}"

