# pylint: disable=missing-module-docstring
import argparse

from .video import Video


def run():
    '''
    provides parsing of the command line.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='bvid or link to the video')
    parser.add_argument('-o', '--offset_cover', type=float,
                        help='the percentage to offset cover')
    parser.add_argument('-ar', '--artist',  help='the artist')
    parser.add_argument('-t', '--title',  help='the artist')
    parser.add_argument('-al', '--album',  help='the album')

    args = parser.parse_args()

    video = Video(args.id)
    for key in ('artist', 'title', 'album'):
        if value := getattr(args, key):
            video.setinfo({key: value})
    cover_offset = args.offset_cover if args.offset_cover else 0.0
    video.download_mp3(
        offset=cover_offset
    )
