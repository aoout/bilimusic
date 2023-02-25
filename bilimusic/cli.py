# pylint: disable=missing-module-docstring,invalid-name
import fire
from .Video import Video


class BiliMusic:
    '''
    command group.
    '''
    def __init__(self, offset:float=0.0) -> None:
        self._offset = offset

    def music(self, id_:str or int, artist:str=None, title:str=None, album:str=None, start:float=None, end:float=None):
        '''
        download the mp3 file.
        '''
        video = Video(id_)

        video.setinfo({key: value for key, value in dict(
            artist=artist,
            title=title,
            album=album
        ).items() if value})

        video.download_mp3(offset=self._offset)

    def cover(self, id_):
        '''
        download the cover.
        '''
        video = Video(id_)
        video.download_cover()
        video.cut_cover(offset=self._offset)


def run():
    '''
    the entry of the program.
    '''
    fire.Fire(BiliMusic)
