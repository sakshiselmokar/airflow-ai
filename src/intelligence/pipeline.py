from src.intelligence.flow_builder import create_graph, build_flow_tree
from src.intelligence.code_generator import generate_code
from src.intelligence.explainer import generate_explanation
from src.intelligence.flow_validator import validate_graph


def run_pipeline(input_data):
    graph = create_graph(input_data)

    # ✅ Validate BEFORE building flow
    errors = validate_graph(graph)

    if errors:
        return {
            "graph": graph,
            "flow": None,
            "code": "INVALID FLOW",
            "explanation": errors
        }

    # ✅ Safe flow building
    flow = build_flow_tree(graph)

    code = generate_code(flow)
    explanation = generate_explanation(flow)

    return {
        "graph": graph,
        "flow": flow,
        "code": code,
        "explanation": explanation
    }