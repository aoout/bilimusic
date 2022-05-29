from tempfile import NamedTemporaryFile

from PIL import Image


def square_imagedata(imagedata: bytes) -> bytes:
    with NamedTemporaryFile(suffix='.jpg', delete=False) as tmp1, NamedTemporaryFile(suffix='.jpg', delete=False) as tmp2:
        tmp1.write(imagedata)
        img = Image.open(tmp1.name).convert('RGB')
        width, height = img.size
        shorter_edge = min(width, height)
        img = img.crop(((width - shorter_edge) // 2,
                        (height - shorter_edge) // 2,
                        (width + shorter_edge) // 2,
                        (height + shorter_edge) // 2))
        img.save(tmp2.name)
        return tmp2.read()
