from collections import defaultdict, Counter

# simple report building with:
def build_report(tickets, results, input_file):
    decisions = Counter(r["final_decision"] for r in results)
    total = len(results)

    # Segment by customer_tier and language_fluency
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