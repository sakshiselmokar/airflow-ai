from src.vision.hand_tracking import HandTracker
from src.intelligence.pipeline import run_pipeline


def main():
    tracker = HandTracker()

    print("🎥 AirFlow AI Started")
    print("Draw → Connect → Press 'e'")

    data = tracker.run()

    if not data:
        print("No data captured")
        return

    result = run_pipeline(data)

    print("\n--- GRAPH ---")
    print(result["graph"])

    print("\n--- FLOW ---")
    print(result["flow"])

    print("\n--- GENERATED CODE ---")
    print(result["code"])

    print("\n--- EXPLANATION ---")
    for line in result["explanation"]:
        print("-", line)


if __name__ == "__main__":
    main()