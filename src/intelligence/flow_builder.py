from src.shared.data_models import Shape, Connection
from src.intelligence.node_builder import build_nodes, build_graph


def parse_input(data):
    shapes = []
    shape_lookup = {}

    # recreate Shape objects
    for s in data["shapes"]:
        shape = Shape(s["type"], tuple(s["center"]), s.get("meaning", "process"))
        shape.text = s.get("text", "")
        shapes.append(shape)
        shape_lookup[(s["type"], tuple(s["center"]))] = shape

    connections = []

    for c in data["connections"]:
        from_key = tuple(c["from"])
        to_key = tuple(c["to"])

        from_shape = shape_lookup.get(from_key)
        to_shape = shape_lookup.get(to_key)

        if from_shape and to_shape:
            connections.append(Connection(from_shape, to_shape))

    return shapes, connections


def create_graph(data):
    shapes, connections = parse_input(data)
    nodes = build_nodes(shapes)
    graph = build_graph(nodes, connections)
    return graph


def traverse_graph(graph):
    edges = graph["edges"]
    nodes = {node["id"]: node for node in graph["nodes"]}

    flow = []

    if not edges:
        return flow

    incoming = set(e["to"] for e in edges)
    start_nodes = [nid for nid in nodes if nid not in incoming]

    current = start_nodes[0] if start_nodes else edges[0]["from"]

    visited = set()

    while current not in visited:
        visited.add(current)

        node = nodes[current]
        flow.append(node)

        # handle multiple outgoing edges (basic)
        outgoing = [e for e in edges if e["from"] == current]

        if not outgoing:
            break

        # for MVP → take first edge
        current = outgoing[0]["to"]

    return flow