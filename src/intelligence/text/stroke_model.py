# import torch
# import torch.nn as nn


# class StrokeLSTM(nn.Module):
#     def __init__(self, input_size=4, hidden_size=128, num_classes=36):
#         super().__init__()

#         self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
#         self.fc = nn.Linear(hidden_size, num_classes)

#     def forward(self, x):
#         # x: (batch, seq_len, 4)
#         out, _ = self.lstm(x)
#         out = out[:, -1, :]  # last time step
#         out = self.fc(out)
#         return out

import torch
import torch.nn as nn


class StrokeLSTM(nn.Module):

    def __init__(
        self,
        input_size=4,
        hidden_size=128,
        num_classes=36
    ):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=2,
            dropout=0.3,
            bidirectional=True,
            batch_first=True
        )

        self.fc1 = nn.Linear(
            hidden_size * 2,
            128
        )

        self.relu = nn.ReLU()

        self.dropout = nn.Dropout(0.3)

        self.fc2 = nn.Linear(
            128,
            num_classes
        )

    def forward(self, x):

        out, _ = self.lstm(x)

        # last sequence output
        out = out[:, -1, :]

        out = self.fc1(out)

        out = self.relu(out)

        out = self.dropout(out)

        out = self.fc2(out)

        return out