'''
implemented some functions unrelated to business logic.
'''

from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
from moviepy.editor import AudioFileClip
from PIL.Image import Image
from PIL.JpegImagePlugin import JpegImageFile
from pydub import AudioSegment
from tqdm import tqdm


def bytes2md(bytes_: int, decimal_places: int = 3) -> float:
    '''
    convert the bytes to md.
    '''
    return round(bytes_/1024 / 1024, decimal_places)


def square_jpeg(img: JpegImageFile, offset: float = 0.0) -> Image:
    '''
    cut the picture into the largest possible square.
    '''
    width, height = img.size
    edge = min(width, height)
    leftover = (max(width, height) - edge)//2
    if edge == height:
        return img.crop((
            leftover + int(leftover * offset),
            0,
            width-leftover + int(leftover * offset),
            height
        ))

    return img.crop((
        0,
        leftover + int(leftover * offset),
        width,
        height-leftover + int(leftover * offset)
    ))


def to_pathname(path: str) -> str:
    '''
    convert a string to a valid windows path.
    '''
    return ''.join([c for c in path if c not in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']])

def download_audio(path: str or Path, url: str, headers: dict) -> None:
    '''
    download a audio from url.
    '''
    path = Path(path)

    with NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        content_length = int(requests.head(
            url, headers=headers).headers['Content-Length'])
        total = bytes2md(content_length)
        with requests.get(url, stream=True, headers=headers) as r:
            with tqdm(total=total, unit='mb') as pbar:
                for chunk in r.iter_content(chunk_size=1024):
                    tmp.write(chunk)
                    pbar.update(bytes2md(len(chunk)))
        AudioFileClip(tmp.name).write_audiofile(str(path), bitrate='192k')

def time2millisec(time: str) -> int:
    '''
    nothing to say. just watch name.
    '''
    _min, sec = time.split(":")
    return (int(_min) * 60 + int(sec))*1000

def extract_audio(audio_file:str or Path, start:str,end:str)->None:
    '''
    extract audio.
    '''
    audio_file = Path(audio_file)
    _as = AudioSegment.from_file(audio_file)
    extract = _as[time2millisec(start):time2millisec(end)]
    extract.export(audio_file.name,format="mp3")