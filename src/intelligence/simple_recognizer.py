import numpy as np

def recognize_digit(img):
    """
    Very basic recognition logic
    """
    non_zero = np.count_nonzero(img)

    # Heuristic rules
    if non_zero < 20:
        return "1"

    height_sum = np.sum(img, axis=1)
    width_sum = np.sum(img, axis=0)

    # If mostly vertical → "1"
    if np.max(width_sum) > np.max(height_sum):
        return "1"

    # If more spread → "0" or "5"
    if non_zero > 100:
        return "0"

    return "5"