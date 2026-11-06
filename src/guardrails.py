import re
from typing import Dict, Any, List
from src.models import Ticket


class Guardrails:
    def __init__(self):
        # Simple patterns that should never appear in an outbound answer
        self.pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",          # SSN-like
            r"\b(?:\d[ -]*?){13,16}\b",        # credit-card like
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email
            r"\b(?:password|secret|api[_-]?key)\s*[:=]\s*\S+",  # leaked secrets
        ]

    def check(
        self,
        ticket: Ticket,
        generated: Dict[str, Any] | None = None
    ) -> Dict[str, str]:
        """
        Returns:
            {"decision": "allow" | "block", "reason": "..."}
        """
        # 1. Hard flag from the dataset
        if ticket.labels.must_not_auto_respond is True:
            return {
                "decision": "block",
                "reason": "Ticket flagged must_not_auto_respond=True"
            }

        # 2. Check generated answer for private data patterns
        if generated and generated.get("answer"):
            answer = generated["answer"]
            for pattern in self.pii_patterns:
                if re.search(pattern, answer, re.IGNORECASE):
                    return {
                        "decision": "block",
                        "reason": f"Potential private data detected in answer (pattern: {pattern})"
                    }

        # 3. Extremely low confidence from generator
        if generated and generated.get("confidence", 1.0) < 0.25:
            return {
                "decision": "block",
                "reason": "Generator confidence too low"
            }

        return {
            "decision": "allow",
            "reason": "Passed all guardrails"
        }