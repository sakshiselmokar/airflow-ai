# HANDTRACKING

import cv2
import mediapipe as mp
import numpy as np
import time
from collections import Counter

from src.vision.gesture_detector import detect_gesture
from src.shared.data_models import Shape, Connection
from src.intelligence.text.stroke_predict import predict_stroke
from src.vision.shape_detector import detect_shape

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def find_nearest_shape(shapes, point):
    if not shapes:
        return None

    px, py = point

    nearest = min(
        shapes,
        key=lambda s: (s.center[0] - px) ** 2 + (s.center[1] - py) ** 2
    )

    dist = (nearest.center[0] - px) ** 2 + (nearest.center[1] - py) ** 2

    if dist < 5000:
        return nearest

    return None


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

        self.points = []
        self.text_points = []
        self.last_text_stroke = []   # 🔥 IMPORTANT FIX

        self.was_drawing = False

        self.prev_x, self.prev_y = 0, 0

        self.shapes = []
        self.connections = []

        self.text_buffer = ""
        self.text_cooldown = 0
        self.last_char_time = time.time()

        self.mode = "idle"

        self.gesture_history = []
        self.last_gesture = None

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

    def undo(self):
        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]

        elif self.connections:
            self.connections.pop()

        elif self.shapes:
            self.shapes.pop()

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

    def is_drawing(self, lm):
        return lm[8].y < lm[6].y and lm[12].y > lm[10].y

    def run(self):
        cap = cv2.VideoCapture(0)

        data = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                lm = results.multi_hand_landmarks[0].landmark

                gesture = detect_gesture(results.multi_hand_landmarks[0])

                if gesture:
                    self.gesture_history.append(gesture)
                    if len(self.gesture_history) > 10:
                        self.gesture_history.pop(0)

                stable = self.get_stable_gesture()
                if stable:
                    self.last_gesture = stable
                    self.mode = self.update_mode(stable)

                    if self.mode == "shape":
                        self.text_points = []

                    elif self.mode == "text":
                        self.points = []

                h, w, _ = frame.shape
                cx = int(lm[8].x * w)
                cy = int(lm[8].y * h)

                cx = int(0.7 * self.prev_x + 0.3 * cx)
                cy = int(0.7 * self.prev_y + 0.3 * cy)
                self.prev_x, self.prev_y = cx, cy

                # ================= SHAPE MODE =================
                if self.mode == "shape":
                    self.text_points = []

                    if self.is_drawing(lm):
                        self.points.append((cx, cy))
                        self.was_drawing = True

                    else:
                        if self.was_drawing:
                            stroke = get_last_stroke(self.points)

                            if len(stroke) > 20:
                                shape_type = detect_shape(stroke)
                                pts = np.array(stroke)

                                center = (
                                    int(np.mean(pts[:, 0])),
                                    int(np.mean(pts[:, 1]))
                                )

                                x, y, w_box, h_box = cv2.boundingRect(pts)

                                if shape_type in ["line", "unknown"] and len(self.shapes) >= 2:
                                    s1 = find_nearest_shape(self.shapes, stroke[0])
                                    s2 = find_nearest_shape(self.shapes, stroke[-1])

                                    if s1 and s2 and s1 != s2:
                                        self.connections.append(Connection(s1, s2))

                                elif shape_type != "unknown":
                                    meaning = "process"

                                    if self.last_gesture == "thumbs_up":
                                        if not any(s.meaning == "start" for s in self.shapes):
                                            meaning = "start"

                                    if shape_type == "diamond":
                                        meaning = "condition"

                                    shape_obj = Shape(shape_type, center, meaning)
                                    shape_obj.bbox = (x, y, w_box, h_box)

                                    self.shapes.append(shape_obj)

                        self.points.append(None)
                        self.was_drawing = False

                # ================= TEXT MODE =================
                elif self.mode == "text":

                    self.points = []

                    if self.is_drawing(lm):
                        self.text_points.append((cx, cy))
                        self.was_drawing = True

                    else:
                        if self.was_drawing and len(self.text_points) > 20:

                            # 🔥 SAVE LAST STROKE
                            self.last_text_stroke = self.text_points.copy()

                            # 🔥 SIMPLE (no segmentation for now)
                            recognized_text = predict_stroke(self.text_points)

                            print("RECOGNIZED:", recognized_text)

                            if recognized_text:
                                from src.intelligence.spatial_mapper import map_text_to_shapes

                                map_text_to_shapes(
                                    self.text_points,
                                    self.shapes,
                                    recognized_text
                                )

                                if time.time() - self.last_char_time > 1:
                                    self.text_buffer += " "

                                self.text_buffer += recognized_text
                                self.last_char_time = time.time()
                                self.text_cooldown = 15

                        self.text_points = []
                        self.was_drawing = False

                mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            if self.text_cooldown > 0:
                self.text_cooldown -= 1

            # ===== DRAW =====
            for i in range(1, len(self.points)):
                if self.points[i - 1] and self.points[i]:
                    cv2.line(frame, self.points[i - 1], self.points[i], (0, 255, 0), 2)

            for i in range(1, len(self.text_points)):
                if self.text_points[i - 1] and self.text_points[i]:
                    cv2.line(frame, self.text_points[i - 1], self.text_points[i], (255, 0, 0), 2)

            for s in self.shapes:
                x, y = s.center

                if s.type == "circle":
                    cv2.circle(frame, (x, y), 30, (255, 0, 0), 3)

                elif s.type == "rectangle":
                    cv2.rectangle(frame, (x - 40, y - 30), (x + 40, y + 30), (255, 0, 0), 3)

                elif s.type == "diamond":
                    pts = np.array([
                        (x, y - 30),
                        (x + 30, y),
                        (x, y + 30),
                        (x - 30, y)
                    ])
                    cv2.polylines(frame, [pts], True, (255, 0, 0), 3)

                label = s.text if s.text else s.type

                cv2.putText(frame, label, (x - 20, y - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            for c in self.connections:
                cv2.arrowedLine(frame, c.from_shape.center, c.to_shape.center, (0, 0, 255), 2)

            cv2.putText(frame, f"Mode: {self.mode}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.putText(frame, f"Text: {self.text_buffer}", (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("AirFlow", frame)

            key = cv2.waitKey(1)

            if key != -1:
                key = key & 0xFF
                print("KEY:", key)

                if key == ord('q'):
                    break

                elif key == ord('s'):
                    import json

                    if not self.last_text_stroke:
                        print("❌ No stroke captured")
                    else:
                        sample = {
                            "points": self.last_text_stroke,
                            "label": "A"
                        }

                        with open("stroke_data.json", "a") as f:
                            f.write(json.dumps(sample) + "\n")

                        print("✅ Saved:", len(self.last_text_stroke), "points")

                elif key == ord('e'):
                    print("EXPORT")
                    data = self.export_data()
                    break

        cap.release()
        cv2.destroyAllWindows()

        return data