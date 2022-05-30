
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

# TODO:从av号形式的链接会进入链接中包含av号而不是bvid的链接。加入对于av号在api中的适配