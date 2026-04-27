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

# EMNIST: labels 1–26 → we convert to 0–25
idx_to_char = {i - 1: chr(i + 64) for i in range(1, 27)}


# -------------------------
# PREDICTION FUNCTION
# -------------------------
def predict_character(img):
    if img is None:
        return ""

    # normalize
    img = img / 255.0

    # tensor
    img = torch.tensor(img, dtype=torch.float32).to(device)
    img = img.unsqueeze(0).unsqueeze(0)  # (1,1,28,28)

    with torch.no_grad():
        output = model(img)

        # prediction
        pred_class = torch.argmax(output, dim=1).item()

        # 🔥 confidence calculation
        probs = torch.softmax(output, dim=1)
        confidence = probs[0][pred_class].item()

    # -------------------------
    # DEBUG
    # -------------------------
    print(f"RAW: {pred_class}, CONF: {confidence:.2f}")

    # -------------------------
    # 🔥 FILTER BAD PREDICTIONS
    # -------------------------
    if confidence < 0.6:
        return ""   # ignore weak predictions

    return idx_to_char.get(pred_class, "")