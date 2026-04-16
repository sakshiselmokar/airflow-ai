def validate_graph(graph):
    errors = []

    nodes = {n["id"]: n for n in graph["nodes"]}
    outgoing = {}

    # build outgoing edge map
    for e in graph["edges"]:
        outgoing.setdefault(e["from"], []).append(e["to"])

    # 🔥 Rule 1: exactly ONE start node
    starts = [n for n in nodes.values() if n["type"] == "start"]
    if len(starts) != 1:
        errors.append("There must be exactly ONE start node")

    # 🔥 Rule 2: only condition can have multiple outputs
    for node_id, outs in outgoing.items():
        if len(outs) > 1:
            node_type = nodes[node_id]["type"]

            if node_type != "condition":
                errors.append(
                    f"Node {node_id} has multiple outputs but is not a condition"
                )

    # 🔥 Rule 3: no isolated nodes
    connected = set()
    for e in graph["edges"]:
        connected.add(e["from"])
        connected.add(e["to"])

    for node_id in nodes:
        if node_id not in connected:
            errors.append(f"Node {node_id} is not connected")

    return errors