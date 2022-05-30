import argparse

from .Video import Video

def run():

    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='bvid or link to the video')
    parser.add_argument('-c', '--cleaner_cover',
                        action='store_true', help='make cover cleaner')
    parser.add_argument('-o', '--offset_cover', type=float,
                        help='the percentage to offset cover')
    parser.add_argument('-ar', '--artist',  help='the artist')
    parser.add_argument('-t', '--title',  help='the artist')
    parser.add_argument('-al', '--album',  help='the album')

    args = parser.parse_args()



    video = Video(args.id, lazyload=True)
    correction = dict()
    if args.artist:
        correction['artist'] = args.artist
    if args.title:
        correction['title'] = args.title
    if args.album:
        correction['album'] = args.album

    video.parse(
        correction=correction
    )
    videopage = video.pages[0]

    cover_offset = 0.0
    if args.offset_cover:
        cover_offset = args.offset_cover

    videopage.download(
        cleaner_cover=args.cleaner_cover,
        cover_offset=cover_offset
    )
