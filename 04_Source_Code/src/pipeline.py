import os
from typing import List, Dict, Any
from src.models import Ticket
from src.classifier import TicketClassifier
from src.retriever import DocumentRetriever
from src.router import Router
from src.generator import AnswerGenerator
from src.guardrails import Guardrails
from src.decision_logger import DecisionLogger


class SupportPipeline:
    def __init__(self, confidence_threshold: float = 0.65):
        self.classifier = TicketClassifier()
        self.retriever = DocumentRetriever()
        self.retriever.build_index()
        self.router = Router(confidence_threshold=confidence_threshold)
        self.generator = AnswerGenerator()
        self.guardrails = Guardrails()
        self.logger = DecisionLogger()

    def process_ticket(self, ticket: Ticket) -> Dict[str, Any]:
        # Check for kill switch
        if os.getenv("AUTO_RESPOND", "true").lower() == "false":
                    final_decision = "escalate"
                    reason = "Kill switch active (AUTO_RESPOND=false)"
                    self.logger.log(
                        ticket=ticket,
                        classification={"intent": None, "urgency": None, "confidence": None},
                        retrieved_docs=[],
                        route_decision={"decision": "escalate", "reason": reason},
                        generation=None,
                        guardrail={"decision": "allow", "reason": "Kill switch – no generation"},
                        final_decision=final_decision
                    )
                    return {
                        "ticket_id": ticket.ticket_id,
                        "final_decision": final_decision,
                        "intent": None,
                        "confidence": None,
                        "citations": [],
                        "reason": reason
                    }
        
        # 1. Classify
        classification = self.classifier.classify(ticket)
        ticket.predicted_intent = classification.get("intent")
        ticket.predicted_urgency = classification.get("urgency")
        ticket.confidence = classification.get("confidence")

        # 2. Retrieve
        query = f"{ticket.subject} {ticket.body[:400]}"
        retrieved = self.retriever.retrieve(query, top_k=4)
        ticket.retrieved_doc_ids = [d["doc_id"] for d in retrieved]

        # 3. Route
        route = self.router.decide(ticket, classification, retrieved)

        # 4. Generate (only if routing says answer)
        generation = None
        if route["decision"] == "answer":
            generation = self.generator.generate(ticket, retrieved)
            ticket.generated_answer = generation.get("answer")
            ticket.citations = generation.get("citations", [])

        # 5. Guardrails
        guard = self.guardrails.check(ticket, generation)
        final_decision = "block" if guard["decision"] == "block" else route["decision"]
        ticket.route_decision = final_decision
        ticket.decision_reason = guard["reason"] if final_decision == "block" else route["reason"]

        # 6. Log
        self.logger.log(
            ticket=ticket,
            classification=classification,
            retrieved_docs=retrieved,
            route_decision=route,
            generation=generation,
            guardrail=guard,
            final_decision=final_decision
        )

        return {
            "ticket_id": ticket.ticket_id,
            "final_decision": final_decision,
            "intent": ticket.predicted_intent,
            "confidence": ticket.confidence,
            "citations": ticket.citations,
            "reason": ticket.decision_reason
        }

    def process_batch(self, tickets: List[Ticket]) -> List[Dict[str, Any]]:
        results = []
        for i, ticket in enumerate(tickets, 1):
            try:
                result = self.process_ticket(ticket)
                results.append(result)
                if i % 10 == 0:
                    print(f"Processed {i}/{len(tickets)}")
            except Exception as e:
                print(f"Error on {ticket.ticket_id}: {e}")
                results.append({
                    "ticket_id": ticket.ticket_id,
                    "final_decision": "error",
                    "reason": str(e)
                })
        return results