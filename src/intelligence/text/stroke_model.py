import torch
import torch.nn as nn


class StrokeLSTM(nn.Module):
    def __init__(self, input_size=4, hidden_size=128, num_classes=36):
        super().__init__()

        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # x: (batch, seq_len, 4)
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # last time step
        out = self.fc(out)
        return out