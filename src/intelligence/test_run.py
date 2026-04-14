from src.intelligence.pipeline import run_pipeline


input_data = {
    "shapes": [
        {"type": "start", "center": [100, 200]},
        {"type": "process", "center": [200, 300]},
        {"type": "condition", "center": [300, 400]}
    ],
    "connections": [[0, 1], [1, 2]]
}


result = run_pipeline(input_data)

print("\n--- GENERATED CODE ---")
print(result["code"])

print("\n--- EXPLANATION ---")
for line in result["explanation"]:
    print("-", line)