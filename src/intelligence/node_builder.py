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
        if shape.meaning == "start":
            node_type = "start"
        elif shape.meaning == "condition":
            node_type = "condition"
        elif shape.meaning == "end":
            node_type = "end"
        else:
            node_type = "process"

        nodes.append({
            "id": i + 1,
            "type": node_type,
            "pos": shape.center
        })    

        
    return nodes

# ✅ ADD THIS FUNCTION
def build_graph(nodes, connections):
    edges = build_edges(connections, nodes)

    return {
        "nodes": nodes,
        "edges": edges
    }

def build_edges(connections, nodes):
    edges = []

    # Map shape center → node id
    shape_to_id = {tuple(node["pos"]): node["id"] for node in nodes}

    for conn in connections:
        from_shape = conn.from_shape
        to_shape = conn.to_shape

        from_id = shape_to_id.get(tuple(from_shape.center))
        to_id = shape_to_id.get(tuple(to_shape.center))

        if from_id and to_id:
            edges.append({
                "from": from_id,
                "to": to_id
            })

    return edges