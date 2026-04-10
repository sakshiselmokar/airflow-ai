import numpy as np

def normalize_stroke(strokes, size=28):
    """
    strokes = [ [(x,y)...], [(x,y)...] ]
    """
    all_points = np.concatenate(strokes)

    min_x, min_y = np.min(all_points, axis=0)
    all_points -= [min_x, min_y]

    max_x, max_y = np.max(all_points, axis=0)
    scale = max(max_x, max_y)

    if scale != 0:
        all_points = all_points / scale

    all_points = all_points * (size - 1)

    normalized = []
    idx = 0

    for stroke in strokes:
        length = len(stroke)
        normalized.append(all_points[idx:idx+length].astype(int))
        idx += length

    return normalized