import cv2
import mediapipe as mp
import numpy as np

from intelligence.stroke_processor import normalize_stroke
from intelligence.image_converter import strokes_to_image
from intelligence.utils import smooth_stroke, interpolate_stroke
from intelligence.recognizer_mnist import predict

# -------------------------------
# Setup MediaPipe
# -------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# -------------------------------
# Variables
# -------------------------------
points = []
drawing = False

# -------------------------------
# Start Camera
# -------------------------------
cap = cv2.VideoCapture(0)

print("Press 'c' to clear | 'p' to predict | 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            # Index finger tip
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Draw circle on fingertip
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Drawing always ON (simple version)
            points.append((x, y))

    # -------------------------------
    # Draw trajectory
    # -------------------------------
    for i in range(len(points) - 1):
        cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 3)

    # -------------------------------
    # Show frame
    # -------------------------------
    cv2.imshow("Air Draw", frame)

    key = cv2.waitKey(1) & 0xFF

    # -------------------------------
    # CLEAR
    # -------------------------------
    if key == ord('c'):
        points = []
        print("Cleared")

    # -------------------------------
    # PREDICT
    # -------------------------------
    elif key == ord('p'):

        if len(points) < 10:
            print("Draw something first")
            continue

        # Convert to stroke format
        stroke = points.copy()

        # Preprocess
        stroke = smooth_stroke(stroke)
        stroke = interpolate_stroke(stroke)

        strokes = [stroke]

        # Normalize
        norm = normalize_stroke(strokes)

        # Convert to image
        img = strokes_to_image(norm)

        # Invert (IMPORTANT)
        img = 255 - img

        # Predict
        digit, confidence, _ = predict(img)

        print(f"Detected: {digit} | Confidence: {confidence:.2f}")

        cv2.imshow("28x28 Input", img)

    # -------------------------------
    # QUIT
    # -------------------------------
    elif key == ord('q'):
        break

# -------------------------------
# Cleanup
# -------------------------------
cap.release()
cv2.destroyAllWindows()