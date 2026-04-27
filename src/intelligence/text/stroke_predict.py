import torch
import numpy as np

from src.intelligence.text.stroke_model import StrokeLSTM
from src.intelligence.text.stroke_utils import stroke_to_sequence, idx_to_char

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = StrokeLSTM().to(device)

# 🔥 load later after training
try:
    model.load_state_dict(torch.load("stroke_model.pth", map_location=device))
    model.eval()
    MODEL_LOADED = True
except:
    print("⚠️ Stroke model not trained yet")
    MODEL_LOADED = False

def predict_stroke(points):
    if not MODEL_LOADED:
        # 🔥 TEMP fallback so UI doesn't break
        return "?"

    seq = stroke_to_sequence(points)

    if seq is None:
        return ""

    seq = torch.tensor(seq).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(seq)
        probs = torch.softmax(out, dim=1)

        pred = torch.argmax(probs, dim=1).item()
        conf = probs[0][pred].item()

    print(f"STROKE PRED: {idx_to_char[pred]}, CONF: {conf:.2f}")

    if conf < 0.5:
        return "?"

    return idx_to_char[pred]
