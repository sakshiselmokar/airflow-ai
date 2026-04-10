def shape_to_node(shape, node_id):
    mapping = {
        "rectangle": "process",
        "circle": "start",
        "line": "connector"
    }

    return {
        "id": node_id,
        "type": mapping.get(shape.type, "unknown"),
        "pos": shape.center
    }


def build_nodes(shapes):
    nodes = []

    for i, shape in enumerate(shapes):
        node = shape_to_node(shape, i + 1)
        nodes.append(node)

    return nodes

# ✅ ADD THIS FUNCTION
def build_graph(nodes):
    return {
        "nodes": nodes,
        "edges": []  # will be filled in Day 4
    }