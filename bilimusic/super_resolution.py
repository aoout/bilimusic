from pathlib import Path

import cv2
from cv2 import dnn_superres


def super_resolution(src: str or Path, dest: str or Path) -> None:

    sr = dnn_superres.DnnSuperResImpl_create()
    image = cv2.imread(src)
    path = "LapSRN_x8.pb"
    sr.readModel(path)
    sr.setModel("lapsrn", 8)
    result = sr.upsample(image)
    cv2.imwrite(dest, result)
