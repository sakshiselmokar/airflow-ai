def generate_code(flow):
    code = ["def flow():"]

    def generate(node, indent="    "):
        if not node:
            return

        t = node["type"]
        text = node.get("text", "")

        safe_text = str(text).replace("'", "").replace("\n", " ")

        if t == "start":
            code.append(indent + "print('Start')")

        elif t == "process":
            if safe_text:
                code.append(indent + f"print('{safe_text}')")
            else:
                code.append(indent + "print('Process')")

        elif t == "condition":
            cond = safe_text if safe_text else "True"

            code.append(indent + f"if {cond}:")

            if node.get("yes"):
                generate(node["yes"], indent + "    ")
            else:
                code.append(indent + "    pass")

            code.append(indent + "else:")

            if node.get("no"):
                generate(node["no"], indent + "    ")
            else:
                code.append(indent + "    pass")

            return

        elif t == "end":
            code.append(indent + "print('End')")

        if "next" in node:
            generate(node["next"], indent)

    generate(flow)

    return "\n".join(code)