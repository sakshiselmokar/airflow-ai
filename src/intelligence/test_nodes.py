from src.shared.data_models import Shape
from src.intelligence.node_builder import build_nodes, build_graph

# Dummy shapes (simulate Person A output)
shapes = [
    Shape("rectangle", (320, 210)),
    Shape("circle", (400, 300)),
    Shape("line", (500, 250))
]

# Convert to nodes
nodes = build_nodes(shapes)

# Build graph
graph = build_graph(nodes)

print("\n--- Nodes ---")
print(nodes)

print("\n--- Graph ---")
print(graph)