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
            "pos": shape.center,
            "text": shape.text if shape.text else ""   # 🔥 FIX
        })

    return nodes


def build_graph(nodes, connections):
    edges = build_edges(connections, nodes)

    return {
        "nodes": nodes,
        "edges": edges
    }


def build_edges(connections, nodes):
    edges = []

    shape_to_id = {tuple(node["pos"]): node["id"] for node in nodes}

    for conn in connections:
        from_id = shape_to_id.get(tuple(conn.from_shape.center))
        to_id = shape_to_id.get(tuple(conn.to_shape.center))

        if from_id and to_id:
            edges.append({
                "from": from_id,
                "to": to_id
            })

    return edges