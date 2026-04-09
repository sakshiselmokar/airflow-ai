from stroke_processor import normalize_stroke
from image_converter import stroke_to_image
from simple_recognizer import recognize_digit

import cv2

# Dummy stroke (simulate "1")
stroke = [
    (10, 10), (10, 20), (10, 30), (10, 40)
]

# Step 1: Normalize
norm_stroke = normalize_stroke(stroke)

# Step 2: Convert to image
img = stroke_to_image(norm_stroke)

# Step 3: Recognize
result = recognize_digit(img)

print("Detected:", result)

# Show image
cv2.imshow("Stroke Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()