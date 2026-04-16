def generate_code(flow):
    code = ["def flow():"]
    
    def generate(node, indent="    "):
        t = node["type"]
        text = node.get("text")

        if t == "start":
            code.append(indent + "print('Start')")

        elif t == "process":
            if text:
                code.append(indent + f"print('{text}')")
            else:
                code.append(indent + "print('Process')")

        elif t == "condition":
            cond = text if text else "True"

            code.append(indent + f"if {cond}:")
            generate(node["yes"], indent + "    ")

            code.append(indent + "else:")
            generate(node["no"], indent + "    ")

            return  # IMPORTANT

        elif t == "end":
            code.append(indent + "print('End')")

        # next chain
        if "next" in node:
            generate(node["next"], indent)

    generate(flow)

    return "\n".join(code)