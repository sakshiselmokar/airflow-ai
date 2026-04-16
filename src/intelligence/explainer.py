def generate_explanation(flow):
    explanation = []

    for step, node in flow:
        if step == "start":
            explanation.append("Start of flow")

        elif step == "process":
            explanation.append(f"Process: {node.get('text', '')}")

        elif step == "condition":
            explanation.append(f"Condition: {node.get('text', '')}")

    return explanation