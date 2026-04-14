def generate_code(flow):
    code = ["def flow():"]

    for step_type, node in flow:

        if step_type == "start":
            code.append("    print('Start')")

        elif step_type == "process":
            if node.get("text"):
                code.append(f"    {node['text']}")
            else:
                code.append("    print('Process Step')")

        elif step_type == "condition":
            if node.get("text"):
                code.append(f"    if {node['text']}:")
                code.append("        pass")
            else:
                code.append("    if condition:")
                code.append("        pass")

        elif step_type == "end":
            code.append("    print('End')")

    return "\n".join(code)