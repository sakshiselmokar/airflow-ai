import numpy as np
import cv2


def angle(pt1, pt2, pt3):
    v1 = pt1 - pt2
    v2 = pt3 - pt2
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    return np.degrees(np.arccos(cos_theta))


def detect_shape(stroke):
    if len(stroke) < 20:
        return "unknown"

    pts = np.array(stroke, dtype=np.int32)

    # Normalize
    pts = pts - np.min(pts, axis=0)
    scale = np.max(pts)
    if scale == 0:
        return "unknown"

    pts = (pts / scale * 400).astype(int)

    img = np.zeros((500, 500), dtype=np.uint8)

    for i in range(1, len(pts)):
        cv2.line(img, tuple(pts[i - 1]), tuple(pts[i]), 255, 2)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return "unknown"

    cnt = max(contours, key=cv2.contourArea)

    perimeter = cv2.arcLength(cnt, True)
    area = cv2.contourArea(cnt)

    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    sides = len(approx)

    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = w / (h + 1e-6)

    # -------------------------
    # LINE (ROBUST FIX)
    # -------------------------
    x, y, w, h = cv2.boundingRect(cnt)

    if max(w, h) > 60:
        ratio = max(w, h) / (min(w, h) + 1e-6)

        if ratio > 2:   # less strict
            return "line"    

    # -------------------------
    # QUADRILATERAL
    # -------------------------
    if 4 <= sides <= 6:   # 🔥 allow imperfect shapes

        pts4 = approx.reshape(-1, 2)

        # side lengths
        sides_len = []
        for i in range(len(pts4)):
            p1 = pts4[i]
            p2 = pts4[(i + 1) % len(pts4)]
            sides_len.append(np.linalg.norm(p1 - p2))

        side_ratio = max(sides_len) / (min(sides_len) + 1e-6)

        # bounding box
        rect_area = w * h
        fill_ratio = area / (rect_area + 1e-6)

        # -------------------------
        # DIAMOND (robust)
        # -------------------------
        if side_ratio < 1.5:  # allow error
            if fill_ratio < 0.75:   # diamond takes less space
                return "diamond"

        # -------------------------
        # RECTANGLE
        # -------------------------
        if fill_ratio > 0.75:
            return "rectangle"

    # -------------------------
    # CIRCLE
    # -------------------------
    if perimeter != 0:
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        if circularity > 0.80:
            return "circle"

    return "unknown"

