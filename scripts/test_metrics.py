from collections import defaultdict, Counter
from src.models import Ticket, TicketLabels, TicketHistory


def build_report(tickets, results, input_file):
    decisions = Counter(r["final_decision"] for r in results)
    total = len(results)

    tier_stats = defaultdict(lambda: Counter())
    fluency_stats = defaultdict(lambda: Counter())

    ticket_map = {t.ticket_id: t for t in tickets}
    for r in results:
        t = ticket_map.get(r["ticket_id"])
        if t:
            tier_stats[t.customer_tier][r["final_decision"]] += 1
            fluency_stats[t.language_fluency][r["final_decision"]] += 1

    report = {
        "input_file": input_file,
        "total_tickets": total,
        "decisions": dict(decisions),
        "answer_rate": decisions.get("answer", 0) / total if total else 0,
        "escalate_rate": decisions.get("escalate", 0) / total if total else 0,
        "block_rate": decisions.get("block", 0) / total if total else 0,
        "error_rate": decisions.get("error", 0) / total if total else 0,
        "by_customer_tier": {k: dict(v) for k, v in tier_stats.items()},
        "by_language_fluency": {k: dict(v) for k, v in fluency_stats.items()},
        "decision_log_entries": len(results),
        "notes": "First full unattended run on validation set"
    }
    return report


# ---------- Synthetic test data ----------
def make_ticket(tid, tier, fluency):
    return Ticket(
        ticket_id=tid,
        channel="email",
        subject="test",
        body="test body",
        received_at="2026-01-01T00:00:00Z",
        customer_id="C1",
        customer_name="Test",
        customer_tier=tier,
        customer_region="na",
        language_fluency=fluency,
        labels=TicketLabels(),
        history=TicketHistory()
    )


tickets = [
    make_ticket("T1", "standard", "fluent"),
    make_ticket("T2", "standard", "non_fluent"),
    make_ticket("T3", "business", "fluent"),
    make_ticket("T4", "enterprise", "fluent"),
    make_ticket("T5", "business", "non_fluent"),
]

results = [
    {"ticket_id": "T1", "final_decision": "answer"},
    {"ticket_id": "T2", "final_decision": "escalate"},
    {"ticket_id": "T3", "final_decision": "answer"},
    {"ticket_id": "T4", "final_decision": "block"},
    {"ticket_id": "T5", "final_decision": "answer"},
]

report = build_report(tickets, results, "dummy_input.json")

import json
print(json.dumps(report, indent=2))

# Basic assertions
assert report["total_tickets"] == 5
assert report["decisions"]["answer"] == 3
assert report["decisions"]["escalate"] == 1
assert report["decisions"]["block"] == 1
assert "standard" in report["by_customer_tier"]
assert "fluent" in report["by_language_fluency"]
print("\nAll checks passed.")