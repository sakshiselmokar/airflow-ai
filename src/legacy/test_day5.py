from src.intelligence.flow_builder import create_graph, traverse_graph, generate_code

# Simulated export data (from Person A)
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

graph = create_graph(data)

print("\n--- GRAPH ---")
print(graph)

flow = traverse_graph(graph)

print("\n--- FLOW ---")
print(flow)

code = generate_code(flow)

print("\n--- GENERATED CODE ---")
print(code)