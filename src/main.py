from src.vision.hand_tracking import HandTracker
from src.intelligence.code_generator import generate_code
from src.intelligence.explainer import generate_explanation
from src.intelligence.flow_builder import create_graph, traverse_graph


def run_pipeline(data):
    print("\n--- RAW DATA ---")
    print(data)

    # ✅ STEP 1: Create graph
    print("\n--- GRAPH ---")
    graph = create_graph(data)
    print(graph)

    # ✅ STEP 2: Traverse graph → ordered nodes
    print("\n--- FLOW (ORDERED NODES) ---")
    flow_nodes = traverse_graph(graph)
    print(flow_nodes)

    # ✅ STEP 3: Convert to (type, node) format
    flow = [(node["type"], node) for node in flow_nodes]

    print("\n--- FLOW (FORMATTED) ---")
    print(flow)

    # ✅ STEP 4: Generate code
    print("\n--- GENERATED CODE ---")
    code = generate_code(flow)
    print(code)

    # ✅ STEP 5: Explanation
    print("\n--- EXPLANATION ---")
    explanation = generate_explanation(flow)
    print(explanation)


def main():
    tracker = HandTracker()

    print("\n🎥 AirFlow AI Started")
    print("👉 Draw shapes")
    print("👉 Connect with lines")
    print("👉 Press 'e' to generate code\n")

    data = tracker.run()

    if data:
        run_pipeline(data)
    else:
        print("No data captured.")


if __name__ == "__main__":
    main()