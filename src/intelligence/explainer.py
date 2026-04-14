def generate_explanation(flow):
    explanation = []

    for step_type, node in flow:

        if step_type == "start":
            explanation.append("Start of the flow")

        elif step_type == "process":
            explanation.append("Process step executed")

        elif step_type == "condition":
            explanation.append("Check a condition")

    return explanation