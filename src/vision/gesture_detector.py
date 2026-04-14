def detect_gesture(hand_landmarks):
    if hand_landmarks is None:
        return None

    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip_id in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [1, 0, 0, 0, 0]:
        return "thumbs_up"

    if fingers == [0, 0, 0, 0, 0]:
        return "fist"

    if fingers == [0, 1, 1, 0, 0]:
        return "two_fingers"

    return None