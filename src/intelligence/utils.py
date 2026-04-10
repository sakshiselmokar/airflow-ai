import numpy as np

def smooth_stroke(stroke, alpha=0.7):
    smoothed = []
    prev_x, prev_y = stroke[0]

    for x, y in stroke:
        new_x = int(alpha * prev_x + (1 - alpha) * x)
        new_y = int(alpha * prev_y + (1 - alpha) * y)
        smoothed.append((new_x, new_y))
        prev_x, prev_y = new_x, new_y

    return smoothed


def interpolate_stroke(stroke, num_points=100):
    stroke = np.array(stroke)
    x = stroke[:, 0]
    y = stroke[:, 1]

    t = np.linspace(0, 1, len(stroke))
    t_new = np.linspace(0, 1, num_points)

    x_new = np.interp(t_new, t, x)
    y_new = np.interp(t_new, t, y)

    return list(zip(x_new.astype(int), y_new.astype(int)))