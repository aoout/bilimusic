from bilimusic import Video

video = Video('https://www.bilibili.com/video/BV1J7411i7Au?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click',lazyload=True)
video.parse(
    correction=dict(
        artist = '谢拉',
        title = '蜜月Un・Deux・Trois'
    )
)
videopage = video.pages[0]
videopage.download()


