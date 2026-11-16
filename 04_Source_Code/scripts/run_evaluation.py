# PSEUDOCODE
# ----------
# 1. Parse CLI args: --input, --output, --threshold (optional).
# 2. Load all tickets from the input JSON file.
# 3. Create SupportPipeline (uses config threshold if not overridden).
# 4. process_batch(tickets) -> list of per-ticket results.
# 5. build_report(tickets, results, input_file) -> metrics dict.
# 6. Write the metrics dict to the output JSON path.
# 7. Print a short summary and the decision-log path.

import argparse
import json
from pathlib import Path
from collections import Counter
from src.data_loader import load_tickets
from src.pipeline import SupportPipeline
from src.metrics import build_report


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

     # Generate the rich metrics dictionary using imported module function
    report = build_report(tickets=tickets, results=results, input_file=args.input)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n=== Evaluation Report ===")
    print(json.dumps(report, indent=2))
    print(f"\nReport written to {args.output}")
    print(f"Decision log: logs/decisions.jsonl ({pipeline.logger.count()} entries)")


if __name__ == "__main__":
    main()