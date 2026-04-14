import numpy as np
from tensorflow.keras.models import load_model

model = load_model("data/models/mnist.h5")

def predict(img):
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)

    pred = model.predict(img)

    probabilities = pred[0]
    digit = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))

    return digit, confidence, probabilities