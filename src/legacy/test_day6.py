from src.intelligence.graph_builder import build_graph_from_export
from src.intelligence.flow_builder import build_flow
from src.intelligence.code_generator import generate_code
from src.intelligence.explainer import explain_flow

# Simulate Person A export
data = {
    "shapes": [
        {"type": "circle", "center": (100, 100)},
        {"type": "rectangle", "center": (200, 200)},
        {"type": "circle", "center": (300, 300)}
    ],
    "connections": [
        {"from": ("circle", (100, 100)), "to": ("rectangle", (200, 200))},
        {"from": ("rectangle", (200, 200)), "to": ("circle", (300, 300))}
    ]
}

graph = build_graph_from_export(data)
flow = build_flow(graph)
code = generate_code(flow)
explanation = explain_flow(flow)

print("\n--- GRAPH ---")
print(graph)

print("\n--- FLOW ---")
print(flow)

print("\n--- GENERATED CODE ---")
print(code)

print("\n--- EXPLANATION ---")
print(explanation)