from src.intelligence.text.predict import predict_character

# fake stroke (draw something roughly like A)
stroke = [(10,10),(15,5),(20,10),(17,8),(13,8)]

print(predict_character(stroke))