import numpy as np
import cv2

def normalize_stroke(points):
    if len(points) < 10:
        return None

    pts = np.array(points)

    # shift to origin
    pts = pts - np.min(pts, axis=0)

    # scale
    max_val = np.max(pts)
    if max_val == 0:
        return None

    pts = (pts / max_val * 20).astype(int)

    # create image
    img = np.zeros((28, 28), dtype=np.uint8)

    for i in range(1, len(pts)):
        cv2.line(img, tuple(pts[i - 1]), tuple(pts[i]), 255, 1)

    return img