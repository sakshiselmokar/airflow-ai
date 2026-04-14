from stroke_processor import normalize_stroke
from image_converter import strokes_to_image
from utils import smooth_stroke, interpolate_stroke
from recognizer_mnist import predict

import cv2

# -------------------------------
# 1. Dummy Stroke Input
# -------------------------------
# Try changing this to test different digits

stroke1 = [(10, 10), (20, 20), (30, 30), (40, 40)]  # diagonal line (may look like 7)
stroke2 = [(40, 10), (40, 40)]  # vertical line

strokes = [stroke1, stroke2]

# -------------------------------
# 2. Preprocessing
# -------------------------------

processed_strokes = []

for stroke in strokes:
    stroke = smooth_stroke(stroke)
    stroke = interpolate_stroke(stroke)
    processed_strokes.append(stroke)

# -------------------------------
# 3. Normalize
# -------------------------------

normalized_strokes = normalize_stroke(processed_strokes)

# -------------------------------
# 4. Convert to Image
# -------------------------------

img = strokes_to_image(normalized_strokes)

# Optional: Invert image (important for MNIST)
img = 255 - img

# -------------------------------
# 5. Predict
# -------------------------------

digit, confidence, probabilities = predict(img)

# -------------------------------
# 6. Output Results
# -------------------------------

print("\n--- Prediction Result ---")

if confidence < 0.6:
    print("⚠️ Uncertain prediction")
else:
    print(f"✅ Detected: {digit}")

print(f"Confidence: {confidence:.2f}")

print("\nAll probabilities:")
for i, p in enumerate(probabilities):
    print(f"{i}: {p:.3f}")

# -------------------------------
# 7. Show Image
# -------------------------------

cv2.imshow("Input to Model (28x28)", img)
cv2.waitKey(0)
cv2.destroyAllWindows()