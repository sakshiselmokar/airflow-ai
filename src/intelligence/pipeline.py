from src.intelligence.graph_builder import build_graph
from src.intelligence.flow_builder import build_flow
from src.intelligence.code_generator import generate_code
from src.intelligence.explainer import generate_explanation


def run_pipeline(input_data):
    shapes = input_data["shapes"]
    connections = input_data["connections"]

    nodes, edges = build_graph(shapes, connections)
    flow = build_flow(nodes, edges)

    code = generate_code(flow)
    explanation = generate_explanation(flow)

    return {
        "code": code,
        "explanation": explanation
    }