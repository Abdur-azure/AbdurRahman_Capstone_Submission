from typing import Dict, Any, List
from src.models import Ticket


class Router:
    def __init__(self, confidence_threshold: float = 0.65):
        """
        confidence_threshold: below this value we escalate.
        You can tune this later during evaluation.
        """
        self.confidence_threshold = confidence_threshold

    def decide(
        self,
        ticket: Ticket,
        classification: Dict[str, Any],
        retrieved_docs: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Returns:
            {
                "decision": "answer" | "escalate" | "block",
                "reason": "..."
            }
        """
        conf = float(classification.get("confidence", 0.0))
        must_not = ticket.labels.must_not_auto_respond is True
        has_retrieval = len(retrieved_docs) > 0

        # 1. Hard block conditions
        if must_not:
            return {
                "decision": "block",
                "reason": "Ticket flagged must_not_auto_respond"
            }

        # 2. No useful retrieval → escalate (safer than inventing)
        if not has_retrieval:
            return {
                "decision": "escalate",
                "reason": "No relevant documentation retrieved"
            }

        # 3. Low confidence → escalate
        if conf < self.confidence_threshold:
            return {
                "decision": "escalate",
                "reason": f"Confidence {conf:.2f} below threshold {self.confidence_threshold}"
            }

        # 4. Otherwise answer
        return {
            "decision": "answer",
            "reason": f"Confidence {conf:.2f} and relevant docs found"
        }