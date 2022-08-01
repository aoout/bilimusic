'''
implemented some functions unrelated to business logic.
'''

from PIL.Image import Image
from PIL.JpegImagePlugin import JpegImageFile


def bytes2md(bytes_: int, decimal_places: int = 3) -> float:
    '''
    convert the bytes to md.
    '''
    return round(bytes_/1024/ 1024, decimal_places)


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