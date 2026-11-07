import argparse
import json
from pathlib import Path
from collections import Counter
from src.data_loader import load_tickets
from src.pipeline import SupportPipeline


def main():
    parser = argparse.ArgumentParser(description="CloudServe Support Evaluation Harness")
    parser.add_argument("--input", required=True, help="Path to tickets JSON file")
    parser.add_argument("--output", required=True, help="Path to write metrics report JSON")
    parser.add_argument("--threshold", type=float, default=0.65, help="Confidence threshold")
    args = parser.parse_args()

    print(f"Loading tickets from {args.input} ...")
    tickets = load_tickets(args.input)
    print(f"Loaded {len(tickets)} tickets")

    pipeline = SupportPipeline(confidence_threshold=args.threshold)
    results = pipeline.process_batch(tickets)

    # Simple metrics
    decisions = Counter(r["final_decision"] for r in results)
    total = len(results)

    report = {
        "input_file": args.input,
        "total_tickets": total,
        "decisions": dict(decisions),
        "answer_rate": decisions.get("answer", 0) / total if total else 0,
        "escalate_rate": decisions.get("escalate", 0) / total if total else 0,
        "block_rate": decisions.get("block", 0) / total if total else 0,
        "error_rate": decisions.get("error", 0) / total if total else 0,
        "results_preview": results[:5]
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n=== Evaluation Report ===")
    print(json.dumps(report, indent=2))
    print(f"\nReport written to {args.output}")
    print(f"Decision log: logs/decisions.jsonl ({pipeline.logger.count()} entries)")


if __name__ == "__main__":
    main()