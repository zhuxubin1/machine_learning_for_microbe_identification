import os

import cv2
from PIL import Image

for file in os.listdir("."):
    if not file.endswith(".png"):
        continue
    img = cv2.imread(file, -1)
    h, w, _ = img.shape
    Image.fromarray(img).save(file, dpi=(600, 600))
