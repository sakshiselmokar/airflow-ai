import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.points = []
        self.prev_x, self.prev_y = 0, 0

    def is_drawing(self, landmarks):
        # Check if only index finger is up
        tips = [8, 12, 16, 20]

        fingers = []

        for tip in tips:
            if landmarks[tip].y < landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        # Only index finger up
        return fingers == [1, 0, 0, 0]

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    h, w, _ = frame.shape
                    lm = hand_landmarks.landmark

                    cx = int(lm[8].x * w)
                    cy = int(lm[8].y * h)

                    # smoothing
                    cx = int(0.7 * self.prev_x + 0.3 * cx)
                    cy = int(0.7 * self.prev_y + 0.3 * cy)

                    self.prev_x, self.prev_y = cx, cy

                    if self.is_drawing(lm):
                        self.points.append((cx, cy))
                    else:
                        self.points.append(None)

                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # draw path
            for i in range(1, len(self.points)):
                if self.points[i - 1] is None or self.points[i] is None:
                    continue
                cv2.line(frame, self.points[i - 1], self.points[i], (0, 255, 0), 3)
            cv2.putText(frame, f"Points: {len(self.points)}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Air Drawing", frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            elif key == ord('c'):
                self.points = []

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()