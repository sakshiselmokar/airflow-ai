import torch
import torch.nn as nn
import torch.optim as optim

from src.intelligence.text.stroke_model import StrokeLSTM
from src.intelligence.text.stroke_utils import stroke_to_sequence, char_to_idx

# 🔥 TEMP DATA (replace later with real)
# format: [(points, label)]
dataset = [
    ([(0,0),(1,1),(2,2),(3,3)], "A"),
]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = StrokeLSTM().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 10

for epoch in range(epochs):
    total_loss = 0

    for points, label in dataset:
        seq = stroke_to_sequence(points)

        if seq is None:
            continue

        x = torch.tensor(seq).unsqueeze(0).to(device)
        y = torch.tensor([char_to_idx[label]]).to(device)

        out = model(x)
        loss = criterion(out, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

torch.save(model.state_dict(), "stroke_model.pth")
print("✅ Stroke model saved")