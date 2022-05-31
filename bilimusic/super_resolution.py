# pylint: disable=missing-module-docstring,invalid-name
from pathlib import Path

import cv2
from cv2 import dnn_superres


def super_resolution(src: str or Path, dest: str or Path, multiple: int = 2) -> None:
    '''
    super-resolution images.
    '''
    sr = dnn_superres.DnnSuperResImpl_create()  # pylint: disable=no-member
    image = cv2.imread(str(src))
    path = f"models/LapSRN_x{multiple}.pb"
    sr.readModel(path)
    sr.setModel("lapsrn", multiple)
    result = sr.upsample(image)
    cv2.imwrite(str(dest), result)
