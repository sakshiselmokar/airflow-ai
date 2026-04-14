import json
import os

FILE_PATH = "shared_data.json"


def save_data(data):
    """
    Save vision output so intelligence layer can read it
    """
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)


def load_data():
    """
    Load latest data for intelligence processing
    """
    if not os.path.exists(FILE_PATH):
        return None

    with open(FILE_PATH, "r") as f:
        return json.load(f)