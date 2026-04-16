import numpy as np
import cv2

def normalize_stroke(points):
    if len(points) < 10:
        return None

    pts = np.array(points)

    # shift to origin
    pts = pts - np.min(pts, axis=0)

    # scale to fit better
    max_val = np.max(pts)
    if max_val == 0:
        return None

    pts = (pts / max_val * 24).astype(int)

    img = np.zeros((28, 28), dtype=np.uint8)

    # 🔥 thicker strokes
    for i in range(1, len(pts)):
        cv2.line(img, tuple(pts[i - 1]), tuple(pts[i]), 255, 2)

    # 🔥 center the drawing
    M = cv2.moments(img)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        shiftx = 14 - cx
        shifty = 14 - cy

        T = np.float32([[1, 0, shiftx], [0, 1, shifty]])
        img = cv2.warpAffine(img, T, (28, 28))

    return img