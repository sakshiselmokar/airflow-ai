from src.shared.data_models import Node, Edge


def build_graph(shapes, connections):
    nodes = []
    edges = []

    # Create nodes
    for i, shape in enumerate(shapes):
        node = Node(i, shape["type"], shape["center"])
        nodes.append(node)

    # Create edges
    for conn in connections:
        edge = Edge(conn[0], conn[1])
        edges.append(edge)

    return nodes, edges