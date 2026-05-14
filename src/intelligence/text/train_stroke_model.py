import json
import torch
import numpy as np

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split

from torch import nn
from torch import optim

from sklearn.metrics import classification_report

from src.intelligence.text.stroke_model import StrokeLSTM
from src.intelligence.text.stroke_utils import (
    stroke_to_sequence,
    char_to_idx,
    idx_to_char
)

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)


# -----------------------------
# DATASET
# -----------------------------

class StrokeDataset(Dataset):

    def __init__(self, files):

        self.X = []
        self.y = []

        for file in files:

            print("Loading:", file)

            with open(file, "r") as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    try:

                        sample = json.loads(line)

                        points = sample["points"]
                        label = sample["label"]

                        seq = stroke_to_sequence(points)

                        if seq is None:
                            continue

                        self.X.append(seq)

                        self.y.append(
                            char_to_idx[label]
                        )

                    except Exception:
                        continue


    def __len__(self):

        return len(self.X)


    def __getitem__(self, idx):

        return (

            torch.tensor(
                self.X[idx],
                dtype=torch.float32
            ),

            torch.tensor(
                self.y[idx]
            )

        )


# -----------------------------
# LOAD FILES
# -----------------------------

files = [

    "stroke_data_sakshi.json",
    "stroke_data_prajakta.json"

]

dataset = StrokeDataset(files)

print(
    "\nSamples:",
    len(dataset)
)

train_size = int(
    len(dataset) * .8
)

test_size = (
    len(dataset)
    - train_size
)

train_data, test_data = random_split(
    dataset,
    [train_size, test_size]
)

train_loader = DataLoader(
    train_data,
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    test_data,
    batch_size=32
)


# -----------------------------
# MODEL
# -----------------------------

model = StrokeLSTM().to(device)

criterion = nn.CrossEntropyLoss()

optimizer = optim.AdamW(
    model.parameters(),
    lr=.0005,
    weight_decay=1e-4
)


# -----------------------------
# TRAIN
# -----------------------------

epochs = 60

for epoch in range(epochs):

    model.train()

    total_loss = 0

    correct = 0
    total = 0

    for x, y in train_loader:

        x = x.to(device)
        y = y.to(device)

        optimizer.zero_grad()

        out = model(x)

        loss = criterion(
            out,
            y
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

        pred = torch.argmax(
            out,
            dim=1
        )

        correct += (
            pred == y
        ).sum().item()

        total += len(y)

    acc = correct / total

    print(
        f"Epoch {epoch+1}"
        f" Loss:{total_loss:.2f}"
        f" Acc:{acc:.3f}"
    )


# -----------------------------
# EVALUATE
# -----------------------------

model.eval()

preds = []
actual = []

with torch.no_grad():

    for x, y in test_loader:

        x = x.to(device)

        out = model(x)

        pred = torch.argmax(
            out,
            dim=1
        )

        preds.extend(
            pred.cpu().numpy()
        )

        actual.extend(
            y.numpy()
        )

print("\nREPORT:\n")

print(
    classification_report(
        actual,
        preds,
        zero_division=0
    )
)


torch.save(
    model.state_dict(),
    "stroke_model.pth"
)

print("\nSaved model")