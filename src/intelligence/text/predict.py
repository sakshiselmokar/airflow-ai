import torch
import numpy as np

from src.intelligence.text.model import CNNModel
from src.intelligence.text.emnist_loader import get_label_map


# -------------------------
# DEVICE
# -------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -------------------------
# LOAD MODEL
# -------------------------
model = CNNModel().to(device)
model.load_state_dict(torch.load("emnist_model.pth", map_location=device))
model.eval()


# -------------------------
# LABEL MAP
# -------------------------
label_map = get_label_map()

# reverse mapping: index → char
idx_to_char = {v: k for k, v in label_map.items()}


# -------------------------
# PREDICTION FUNCTION
# -------------------------
def predict_character(img):
    """
    Input: 28x28 image (numpy array)
    Output: predicted character (string)
    """

    if img is None:
        return ""

    # 🔥 normalize (0–1)
    img = img / 255.0

    # 🔥 convert to tensor
    img = torch.tensor(img, dtype=torch.float32).to(device)

    # 🔥 reshape → (batch, channel, height, width)
    img = img.unsqueeze(0).unsqueeze(0)   # (1, 1, 28, 28)

    # 🔥 inference
    with torch.no_grad():
        output = model(img)
        pred_class = torch.argmax(output, dim=1).item()

    # 🔥 confidence check (optional but useful)
    probs = torch.softmax(output, dim=1)
    confidence = probs[0][pred_class].item()

    if confidence < 0.5:
        return ""   # ignore bad predictions

    return idx_to_char.get(pred_class, "")