'''
implemented some functions unrelated to business logic.
'''

from PIL.JpegImagePlugin import JpegImageFile
from PIL.Image import Image


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
