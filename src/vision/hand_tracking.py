import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def find_nearest_shape(shapes, point):
    if not shapes:
        return None

    px, py = point
    min_dist = float('inf')
    nearest = None

    for shape in shapes:
        sx, sy = shape.center
        dist = (sx - px) ** 2 + (sy - py) ** 2

        if dist < min_dist:
            min_dist = dist
            nearest = shape

    return nearest


class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.points = []
        self.prev_x, self.prev_y = 0, 0
        self.was_drawing = False

        # ✅ Day 3
        self.shapes = []

        # ✅ Day 4
        self.connections = []

    def is_drawing(self, landmarks):
        tips = [8, 12, 16, 20]
        fingers = []

        for tip in tips:
            if landmarks[tip].y < landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

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
                        self.was_drawing = True

                    else:
                        # ✅ stroke completed
                        if self.was_drawing:
                            stroke = get_last_stroke(self.points)

                            if len(stroke) > 20:
                                from src.vision.shape_detector import detect_shape
                                from src.shared.data_models import Shape, Connection

                                shape_type = detect_shape(stroke)

                                pts = np.array(stroke)
                                start_point = tuple(pts[0])
                                end_point = tuple(pts[-1])

                                # 🔥 LINE = CONNECTION
                                if shape_type == "line" and len(self.shapes) >= 2:

                                    from_shape = find_nearest_shape(self.shapes, start_point)
                                    to_shape = find_nearest_shape(self.shapes, end_point)

                                    if from_shape and to_shape and from_shape != to_shape:
                                        conn = Connection(from_shape, to_shape)
                                        self.connections.append(conn)

                                        print("Connection:", conn)

                                # 🔥 NORMAL SHAPES
                                elif shape_type != "unknown":
                                    cx = int(np.mean(pts[:, 0]))
                                    cy = int(np.mean(pts[:, 1]))

                                    shape_obj = Shape(shape_type, (cx, cy))
                                    self.shapes.append(shape_obj)

                                    print("Stored:", shape_obj)

                        self.points.append(None)
                        self.was_drawing = False

                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # draw path
            for i in range(1, len(self.points)):
                if self.points[i - 1] is None or self.points[i] is None:
                    continue
                cv2.line(frame, self.points[i - 1], self.points[i], (0, 255, 0), 3)

            # ✅ SHOW SHAPES
            y_offset = 60
            for s in self.shapes:
                text = f"{s.type} at {s.center}"
                cv2.putText(frame, text, (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                y_offset += 25

            # ✅ SHOW CONNECTIONS
            y_offset += 20
            for c in self.connections:
                text = f"{c.from_shape.type} -> {c.to_shape.type}"
                cv2.putText(frame, text, (10, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                y_offset += 25

            cv2.putText(frame, f"Points: {len(self.points)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Air Drawing", frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            elif key == ord('c'):
                self.points = []
                self.shapes = []
                self.connections = []  # ✅ clear all

        cap.release()
        cv2.destroyAllWindows()


def get_last_stroke(points):
    stroke = []

    for p in reversed(points):
        if p is None:
            break
        stroke.append(p)

    return stroke[::-1]


if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()