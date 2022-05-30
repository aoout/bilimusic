from bilimusic import Video

video = Video('https://www.bilibili.com/video/BV1cx411c79i?spm_id_from=333.337.search-card.all.click',lazyload=True)
video.parse(
    correction=dict(
        artist = '洛天依',
        title = '一半一半'
    )
)
videopage = video.pages[0]
videopage.download()