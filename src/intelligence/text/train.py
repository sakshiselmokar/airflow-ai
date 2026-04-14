import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

from emnist_loader import load_emnist
from model import CNNModel

# load data
dataset = load_emnist()
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNNModel().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# training loop
epochs = 3  # start small

for epoch in range(epochs):
    total_loss = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        # 🔥 FIX LABELS (1–26 → 0–25)
        labels = labels - 1

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# save model
torch.save(model.state_dict(), "emnist_model.pth")
print("Model saved!")