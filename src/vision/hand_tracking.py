import cv2
import mediapipe as mp
import numpy as np
import time
from collections import Counter

from src.vision.gesture_detector import detect_gesture
from src.shared.gesture_map import GESTURE_TO_MEANING
from src.shared.data_models import Shape, Connection
from src.intelligence.text.predict import predict_character
from src.intelligence.text.preprocess import normalize_stroke
from src.vision.shape_detector import detect_shape

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


def get_last_stroke(points):
    stroke = []
    for p in reversed(points):
        if p is None:
            break
        stroke.append(p)
    return stroke[::-1]


class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        # Drawing
        self.points = []
        self.text_points = []
        self.was_drawing = False

        self.prev_x, self.prev_y = 0, 0

        # Data
        self.shapes = []
        self.connections = []

        # Text
        self.text_buffer = ""
        self.text_cooldown = 0
        self.last_char_time = time.time()

        # Mode
        self.mode = "idle"

        # Gesture stability
        self.gesture_history = []
        self.last_gesture = None

    # -------------------------
    # Gesture helpers
    # -------------------------
    def get_stable_gesture(self):
        if not self.gesture_history:
            return None

        g, count = Counter(self.gesture_history).most_common(1)[0]
        return g if count >= 3 else None

    def update_mode(self, gesture):
        if gesture == "two_fingers":
            return "text"
        elif gesture == "thumbs_up":
            return "shape"
        elif gesture == "fist":
            return "idle"
        return self.mode

    # -------------------------
    # Undo
    # -------------------------
    def undo(self):
        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]
            print("UNDO TEXT")

        elif self.connections:
            removed = self.connections.pop()
            print("UNDO CONNECTION:", removed)

        elif self.shapes:
            removed = self.shapes.pop()
            print("UNDO SHAPE:", removed)

    # -------------------------
    # Export
    # -------------------------
    def export_data(self):
        return {
            "shapes": [
                {
                    "type": s.type,
                    "meaning": s.meaning,
                    "center": s.center,
                    "text": getattr(s, "text", "")
                }
                for s in self.shapes
            ],
            "connections": [
                {
                    "from": (c.from_shape.type, c.from_shape.center),
                    "to": (c.to_shape.type, c.to_shape.center)
                }
                for c in self.connections
            ]
        }

    # -------------------------
    def is_drawing(self, lm):
        return lm[8].y < lm[6].y and lm[12].y > lm[10].y

    # -------------------------
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
                lm = results.multi_hand_landmarks[0].landmark

                # Gesture detection
                gesture = detect_gesture(results.multi_hand_landmarks[0])

                if gesture:
                    self.gesture_history.append(gesture)
                    if len(self.gesture_history) > 10:
                        self.gesture_history.pop(0)

                stable = self.get_stable_gesture()
                if stable:
                    self.last_gesture = stable
                    self.mode = self.update_mode(stable)

                # Coordinates
                h, w, _ = frame.shape
                cx = int(lm[8].x * w)
                cy = int(lm[8].y * h)

                # smoothing
                cx = int(0.7 * self.prev_x + 0.3 * cx)
                cy = int(0.7 * self.prev_y + 0.3 * cy)
                self.prev_x, self.prev_y = cx, cy

                # ================= SHAPE MODE =================
                if self.mode == "shape":
                    if self.is_drawing(lm):
                        self.points.append((cx, cy))
                        self.was_drawing = True

                    else:
                        if self.was_drawing:
                            stroke = get_last_stroke(self.points)

                            if len(stroke) > 20:
                                shape_type = detect_shape(stroke)
                                pts = np.array(stroke)
                                center = (int(np.mean(pts[:, 0])), int(np.mean(pts[:, 1])))

                                if shape_type == "line" and len(self.shapes) >= 2:
                                    s1 = find_nearest_shape(self.shapes, stroke[0])
                                    s2 = find_nearest_shape(self.shapes, stroke[-1])

                                    if s1 and s2 and s1 != s2:
                                        self.connections.append(Connection(s1, s2))
                                        print("Connection created")

                                elif shape_type != "unknown":
                                    meaning = GESTURE_TO_MEANING.get(self.last_gesture, "process")
                                    shape_obj = Shape(shape_type, center, meaning)
                                    self.shapes.append(shape_obj)
                                    print("Stored:", shape_obj)

                        self.points.append(None)
                        self.was_drawing = False
                elif self.mode == "text":
                    if self.is_drawing(lm):
                        self.text_points.append((cx, cy))
                        self.was_drawing = True

                    else:
                        if (
                            self.was_drawing
                            and len(self.text_points) > 40
                            and self.text_cooldown == 0
                        ):
                            img = normalize_stroke(self.text_points)

                            if img is not None:
                                char = predict_character(img)

                                # 🔥 SAFETY: ignore garbage predictions
                                if char and isinstance(char, str) and len(char) == 1:

                                    # spacing logic
                                    if time.time() - self.last_char_time > 1:
                                        self.text_buffer += " "

                                    self.text_buffer += char
                                    self.last_char_time = time.time()
                                    self.text_cooldown = 15

                                    print("TEXT:", self.text_buffer)

                                    # 🔥 FIX: SAFE TEXT ASSIGNMENT
                                    nearest = find_nearest_shape(self.shapes, self.text_points[0])
                                    if nearest:
                                        if not hasattr(nearest, "text") or nearest.text is None:
                                            nearest.text = ""

                                        nearest.text += char

                        # reset stroke
                        self.text_points = []
                        self.was_drawing = False
                
                mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            # cooldown
            if self.text_cooldown > 0:
                self.text_cooldown -= 1

            # draw strokes
            for i in range(1, len(self.points)):
                if self.points[i - 1] and self.points[i]:
                    cv2.line(frame, self.points[i - 1], self.points[i], (0, 255, 0), 2)

            for i in range(1, len(self.text_points)):
                cv2.line(frame, self.text_points[i - 1], self.text_points[i], (255, 0, 0), 2)

            # draw shapes
            for s in self.shapes:
                x, y = s.center

                if s.type == "circle":
                    cv2.circle(frame, (x, y), 30, (255, 0, 0), 3)

                elif s.type == "rectangle":
                    cv2.rectangle(frame, (x - 40, y - 30), (x + 40, y + 30), (255, 0, 0), 3)

                label = s.text if hasattr(s, "text") and s.text else s.type

                cv2.putText(frame, label, (x - 20, y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # connections
            for c in self.connections:
                cv2.arrowedLine(frame, c.from_shape.center, c.to_shape.center, (0, 0, 255), 2)

            # UI
            cv2.putText(frame, f"Mode: {self.mode}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.putText(frame, f"Text: {self.text_buffer}", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.putText(frame, "C: Clear | U: Undo | E: Export | Q: Quit",
                        (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            cv2.imshow("AirFlow", frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break

            elif key == ord('c'):
                print("CLEAR ALL")
                self.points = []
                self.text_points = []
                self.text_buffer = ""
                self.shapes = []
                self.connections = []
                self.was_drawing = False

            elif key == ord('u'):
                self.undo()

            elif key == ord('e'):
                data = self.export_data()
                cap.release()
                cv2.destroyAllWindows()
                return data

        cap.release()
        cv2.destroyAllWindows()