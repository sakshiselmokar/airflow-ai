from torchvision import datasets, transforms

def load_emnist():
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor()
    ])

    dataset = datasets.EMNIST(
        root='./data',
        split='letters',   # 👈 IMPORTANT (only A-Z)
        train=True,
        download=True,
        transform=transform
    )

    return dataset


# 🔥 ADD THIS FUNCTION
def get_label_map():
    # EMNIST letters: labels 1–26 → A–Z
    return {i: chr(i + 64) for i in range(1, 27)}