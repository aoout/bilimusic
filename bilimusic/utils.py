from PIL.JpegImagePlugin import JpegImageFile


def square_jpeg(img: JpegImageFile, offset: float = 0.0) -> JpegImageFile:

    width, height = img.size
    edge = min(width, height)
    leftover = (max(width, height) - edge)//2
    if edge == height:
        return img.crop((
            leftover + leftover * offset,
            0,
            width-leftover + leftover * offset,
            height
        ))
    else:
        return img.crop((
            0,
            leftover + leftover * offset,
            width,
            height-leftover + leftover * offset
        ))
