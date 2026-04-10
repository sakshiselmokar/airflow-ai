from src.shared.data_models import Shape, Connection
from src.intelligence.node_builder import build_nodes, build_graph

# Shapes
shape1 = Shape("rectangle", (320, 210))
shape2 = Shape("circle", (400, 300))

shapes = [shape1, shape2]

# 🔥 NOW using Connection class
connections = [
    Connection(shape1, shape2)
]

nodes = build_nodes(shapes)
graph = build_graph(nodes, connections)

print("\n--- Nodes ---")
print(nodes)

print("\n--- Graph ---")
print(graph)