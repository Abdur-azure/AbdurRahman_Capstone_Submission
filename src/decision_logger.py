import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from src.models import Ticket


class DecisionLogger:
    def __init__(self, log_path: str = "logs/decisions.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        ticket: Ticket,
        classification: Dict[str, Any],
        retrieved_docs: list,
        route_decision: Dict[str, str],
        generation: Optional[Dict[str, Any]] = None,
        guardrail: Optional[Dict[str, str]] = None,
        final_decision: str = None
    ) -> None:
        """
        Append one complete decision record as a JSON line.
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ticket_id": ticket.ticket_id,
            "channel": ticket.channel,
            "customer_tier": ticket.customer_tier,
            "language_fluency": ticket.language_fluency,
            "classification": {
                "intent": classification.get("intent"),
                "urgency": classification.get("urgency"),
                "confidence": classification.get("confidence")
            },
            "retrieval": {
                "num_docs": len(retrieved_docs),
                "doc_ids": [d.get("doc_id") for d in retrieved_docs]
            },
            "route": route_decision,
            "generation": {
                "answer_preview": (generation.get("answer") or "")[:200] if generation else None,
                "citations": generation.get("citations") if generation else [],
                "confidence": generation.get("confidence") if generation else None
            } if generation else None,
            "guardrail": guardrail,
            "final_decision": final_decision or route_decision.get("decision")
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def count(self) -> int:
        """Return number of logged decisions."""
        if not self.log_path.exists():
            return 0
        with open(self.log_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)