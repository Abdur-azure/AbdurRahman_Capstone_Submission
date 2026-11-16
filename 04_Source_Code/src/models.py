# PSEUDOCODE
# ----------
# 1. Define TicketLabels (intent, urgency, flags, expected docs).
# 2. Define TicketHistory (FCR, CSAT, escalated, etc.).
# 3. Define Ticket:
#    - identity + channel + text + customer info
#    - labels + history
#    - empty fields for later predictions (intent, confidence, answer, citations, route)
# 4. Provide to_dict() so a ticket can be saved or logged easily.

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class TicketLabels:
    intent: Optional[str] = None
    urgency: Optional[str] = None
    expected_route: Optional[str] = None
    answerable_from_docs: Optional[bool] = None
    expected_doc_ids: List[str] = field(default_factory=list)
    must_not_auto_respond: Optional[bool] = None


@dataclass
class TicketHistory:
    first_contact_resolution: Optional[bool] = None
    resolution_time_minutes: Optional[int] = None
    csat_rating: Optional[float] = None
    escalated: Optional[bool] = None
    repeat_contact: Optional[bool] = None


@dataclass
class Ticket:
    """Normalised internal representation used by the whole system."""
    ticket_id: str
    channel: str
    subject: str
    body: str
    received_at: str
    customer_id: str
    customer_name: str
    customer_tier: str
    customer_region: str
    language_fluency: str
    labels: TicketLabels
    history: TicketHistory

    # Fields that will be filled by the system later
    predicted_intent: Optional[str] = None
    predicted_urgency: Optional[str] = None
    confidence: Optional[float] = None
    retrieved_doc_ids: List[str] = field(default_factory=list)
    generated_answer: Optional[str] = None
    citations: List[str] = field(default_factory=list)
    route_decision: Optional[str] = None   # "answer" | "escalate" | "block"
    decision_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "received_at": self.received_at,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_tier": self.customer_tier,
            "customer_region": self.customer_region,
            "language_fluency": self.language_fluency,
            "labels": {
                "intent": self.labels.intent,
                "urgency": self.labels.urgency,
                "expected_route": self.labels.expected_route,
                "answerable_from_docs": self.labels.answerable_from_docs,
                "expected_doc_ids": self.labels.expected_doc_ids,
                "must_not_auto_respond": self.labels.must_not_auto_respond,
            },
            "history": {
                "first_contact_resolution": self.history.first_contact_resolution,
                "resolution_time_minutes": self.history.resolution_time_minutes,
                "csat_rating": self.history.csat_rating,
                "escalated": self.history.escalated,
                "repeat_contact": self.history.repeat_contact,
            },
            "predicted_intent": self.predicted_intent,
            "predicted_urgency": self.predicted_urgency,
            "confidence": self.confidence,
            "retrieved_doc_ids": self.retrieved_doc_ids,
            "generated_answer": self.generated_answer,
            "citations": self.citations,
            "route_decision": self.route_decision,
            "decision_reason": self.decision_reason,
        }