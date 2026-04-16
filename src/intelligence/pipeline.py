from src.intelligence.flow_builder import create_graph, traverse_graph
from src.intelligence.code_generator import generate_code
from src.intelligence.explainer import generate_explanation


def run_pipeline(input_data):
    graph = create_graph(input_data)
    flow = traverse_graph(graph)

    code = generate_code(flow)
    explanation = generate_explanation(flow)

    return {
        "graph": graph,
        "flow": flow,
        "code": code,
        "explanation": explanation
    }