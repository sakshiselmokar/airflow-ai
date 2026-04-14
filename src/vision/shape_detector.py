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

    # Approximate shape
    epsilon = 0.03 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    sides = len(approx)

    # 🔥 LINE detection
    # x, y, w, h = cv2.boundingRect(cnt)
    # 🔥 LINE detection (better)
    x, y, w, h = cv2.boundingRect(cnt)

    aspect_ratio = max(w, h) / (min(w, h) + 1e-6)
    area = cv2.contourArea(cnt)

    # long + thin shape
    if aspect_ratio > 5 and area < 3000:
        return "line"    
    # if h < 15 or w < 15:
    #     return "line"

    # 🔥 RECTANGLE detection using ANGLES
    if sides == 4:
        pts = approx.reshape(4, 2)

        angles = []
        for i in range(4):
            a = pts[i]
            b = pts[(i + 1) % 4]
            c = pts[(i + 2) % 4]

            ang = angle(a, b, c)
            angles.append(ang)

        # check near 90 degrees
        if all(70 < ang < 110 for ang in angles):
            return "rectangle"

    # 🔥 CIRCLE detection (fallback)
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    if perimeter == 0:
        return "unknown"

    circularity = 4 * np.pi * (area / (perimeter * perimeter))

    if circularity > 0.6:
        return "circle"

    return "unknown"