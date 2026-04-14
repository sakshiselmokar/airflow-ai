import torch
import numpy as np
import cv2

from src.intelligence.text.model import CNNModel
from src.intelligence.text.emnist_loader import get_label_map


# load model once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = CNNModel().to(device)
model.load_state_dict(torch.load("emnist_model.pth", map_location=device))
model.eval()

label_map = get_label_map()


def stroke_to_image(stroke, size=28):
    pts = np.array(stroke)

    # normalize
    pts = pts - np.min(pts, axis=0)
    scale = np.max(pts)

    if scale == 0:
        return None

    pts = (pts / scale * (size - 5)).astype(int)

    img = np.zeros((size, size), dtype=np.uint8)

    for i in range(1, len(pts)):
        cv2.line(img, tuple(pts[i - 1]), tuple(pts[i]), 255, 2)

    return img


def predict_character(stroke):
    img = stroke_to_image(stroke)

    if img is None:
        return ""

    img = img / 255.0
    img = img.reshape(1, 1, 28, 28)

    img_tensor = torch.tensor(img, dtype=torch.float32).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        pred = torch.argmax(output, dim=1).item()

    return label_map[pred + 1]   # +1 because EMNIST mapping