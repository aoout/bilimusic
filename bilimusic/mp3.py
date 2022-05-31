# pylint: disable=missing-module-docstring

from pathlib import Path
import eyed3


class Mp3:
    '''
    manage the tags, cover of mp3 file.
    '''

    def __init__(self, path: str or Path) -> None:
        path = Path(path)
        self.path = path
        self.audiofile = eyed3.load(path)

    def settags_withdict(self, dict_: dict) -> None:
        '''
        set the tags of mp3 file with a dict.
        '''
        for key, value in dict_.items():
            setattr(self.audiofile.tag, key, value)
        self.audiofile.tag.save()

    def get_cover(self) -> bytes:
        '''
        return the binary data of mp3 file's cover.
        '''
        return self.audiofile.tag.images.get("cover").data

    def get_cover_tofile(self, path: str or Path = None) -> None:
        '''
        extract the cover of mp3 file to a image file.
        '''
        path = Path(path) if path else self.path.with_suffix('jpg')
        path.write_bytes(self.get_cover())

    def set_cover(self, imagedata: bytes) -> None:
        '''
        set the cover of a mp3 file with binary data.
        '''
        self.audiofile.tag.images.set(3, imagedata, 'image/jpeg', 'cover')
        self.audiofile.tag.save()

    def set_cover_fromfile(self, path: str or Path = None) -> None:
        '''
        set the cover of a mp3 file with a image file.
        '''
        path = Path(path) if path else self.path.with_suffix('jpg')
        imagedata = path.read_bytes()
        self.set_cover(imagedata)
