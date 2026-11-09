import json
from collections import Counter

with open("outputs/validation_report.json") as f:
    report = json.load(f)

print("=== Current Validation Results ===")
print(f"Total tickets : {report['total_tickets']}")
print(f"Answer rate   : {report['answer_rate']:.1%}")
print(f"Escalate rate : {report['escalate_rate']:.1%}")
print(f"Block rate    : {report['block_rate']:.1%}")
print(f"Error rate    : {report['error_rate']:.1%}")

print("\nBy customer tier:")
for tier, stats in report.get("by_customer_tier", {}).items():
    total = sum(stats.values())
    ans = stats.get("answer", 0) / total if total else 0
    print(f"  {tier:12} answer={ans:.1%}  (n={total})")

print("\nBy language fluency:")
for flu, stats in report.get("by_language_fluency", {}).items():
    total = sum(stats.values())
    ans = stats.get("answer", 0) / total if total else 0
    print(f"  {flu:12} answer={ans:.1%}  (n={total})")