def generate_explanation(flow):
    explanation = []

    def traverse(node):
        if not node:
            return

        step = node.get("type")
        text = node.get("text")

        if step == "start":
            explanation.append("Start of flow")

        elif step == "process":
            explanation.append(f"Process: {text if text else 'No operation'}")

        elif step == "condition":
            explanation.append(f"Condition: {text if text else 'No condition'}")

            traverse(node.get("yes"))
            traverse(node.get("no"))
            return  # important

        elif step == "end":
            explanation.append("End of flow")

        elif step == "loop":
            explanation.append("Loop detected")

        # continue linear flow
        traverse(node.get("next"))

    traverse(flow)
    return explanation