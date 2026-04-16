from src.intelligence.text.predict import predict_character
from src.intelligence.text.preprocess import normalize_stroke

stroke = [(10,10),(15,5),(20,10),(17,8),(13,8)]

img = normalize_stroke(stroke)

print(predict_character(img))