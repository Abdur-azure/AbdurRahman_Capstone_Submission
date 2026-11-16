# PSEUDOCODE
# ----------
# 1. Open a tickets JSON file.
# 2. For each raw ticket:
#    - Read labels into TicketLabels
#    - Read history into TicketHistory
#    - Build one normalised Ticket object
# 3. Return the list of Ticket objects.
# 4. Helper: count how many tickets per channel (for quick checks).

import json
from pathlib import Path
from typing import List, Union
from src.models import Ticket, TicketLabels, TicketHistory


def load_tickets(file_path: Union[str, Path]) -> List[Ticket]:
    """
    Load tickets from a JSON file and normalise them into the internal Ticket schema.
    Works for development_tickets.json, validation_tickets.json and the hidden set.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Ticket file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw_tickets = json.load(f)

    tickets: List[Ticket] = []
    for raw in raw_tickets:
        labels_raw = raw.get("labels", {})
        history_raw = raw.get("history", {})

        labels = TicketLabels(
            intent=labels_raw.get("intent"),
            urgency=labels_raw.get("urgency"),
            expected_route=labels_raw.get("expected_route"),
            answerable_from_docs=labels_raw.get("answerable_from_docs"),
            expected_doc_ids=labels_raw.get("expected_doc_ids") or [],
            must_not_auto_respond=labels_raw.get("must_not_auto_respond"),
        )

        history = TicketHistory(
            first_contact_resolution=history_raw.get("first_contact_resolution"),
            resolution_time_minutes=history_raw.get("resolution_time_minutes"),
            csat_rating=history_raw.get("csat_rating"),
            escalated=history_raw.get("escalated"),
            repeat_contact=history_raw.get("repeat_contact"),
        )

        ticket = Ticket(
            ticket_id=raw["ticket_id"],
            channel=raw["channel"],
            subject=raw.get("subject") or "",
            body=raw.get("body") or "",
            received_at=raw.get("received_at") or "",
            customer_id=raw.get("customer_id") or "",
            customer_name=raw.get("customer_name") or "",
            customer_tier=raw.get("customer_tier") or "",
            customer_region=raw.get("customer_region") or "",
            language_fluency=raw.get("language_fluency") or "",
            labels=labels,
            history=history,
        )
        tickets.append(ticket)

    return tickets


def channel_counts(tickets: List[Ticket]) -> dict:
    """Helper for quick verification."""
    from collections import Counter
    return dict(Counter(t.channel for t in tickets))