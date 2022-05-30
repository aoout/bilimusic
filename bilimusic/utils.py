from PIL.JpegImagePlugin import JpegImageFile


def square_jpeg(img: JpegImageFile) -> JpegImageFile:
    width, height = img.size
    shorter_edge = min(width, height)
    img = img.crop(((width - shorter_edge) // 2,
                    (height - shorter_edge) // 2,
                    (width + shorter_edge) // 2,
                    (height + shorter_edge) // 2))
    return img
