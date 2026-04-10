import numpy as np
import cv2

def strokes_to_image(strokes, size=28):
    img = np.zeros((size, size), dtype=np.uint8)

    for stroke in strokes:
        for i in range(len(stroke) - 1):
            x1, y1 = stroke[i]
            x2, y2 = stroke[i + 1]

            cv2.line(img, (x1, y1), (x2, y2), 255, 2)

    return img