import numpy as np

def normalize_stroke(stroke, size=28):
    """
    Normalize stroke to fit into a size x size grid
    """
    stroke = np.array(stroke)

    # Shift to origin
    min_x, min_y = np.min(stroke, axis=0)
    stroke -= [min_x, min_y]

    # Scale to fit
    max_x, max_y = np.max(stroke, axis=0)
    scale = max(max_x, max_y)

    if scale != 0:
        stroke = stroke / scale

    # Scale to grid size
    stroke = stroke * (size - 1)

    return stroke.astype(int)