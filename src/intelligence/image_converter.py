import numpy as np
import cv2

def stroke_to_image(stroke, size=28):
    """
    Convert stroke points into 28x28 image
    """
    img = np.zeros((size, size), dtype=np.uint8)

    for i in range(len(stroke) - 1):
        x1, y1 = stroke[i]
        x2, y2 = stroke[i + 1]

        cv2.line(img, (x1, y1), (x2, y2), 255, 1)

    return img