from src.data_loader import load_tickets
from src.classifier import TicketClassifier
from src.retriever import DocumentRetriever
from src.router import Router
from src.generator import AnswerGenerator
from src.guardrails import Guardrails
from src.decision_logger import DecisionLogger

tickets = load_tickets("data/development_tickets.json")
classifier = TicketClassifier()
retriever = DocumentRetriever()
retriever.build_index()
router = Router()
generator = AnswerGenerator()
guard = Guardrails()
logger = DecisionLogger()

# Process a small batch and log everything
for t in tickets[:5]:
    classification = classifier.classify(t)
    docs = retriever.retrieve(f"{t.subject} {t.body[:300]}", top_k=3)
    route = router.decide(t, classification, docs)

    generation = None
    if route["decision"] == "answer":
        generation = generator.generate(t, docs)

    guardrail_result = guard.check(t, generation)
    final = "block" if guardrail_result["decision"] == "block" else route["decision"]

    logger.log(
        ticket=t,
        classification=classification,
        retrieved_docs=docs,
        route_decision=route,
        generation=generation,
        guardrail=guardrail_result,
        final_decision=final
    )
    print(f"Logged {t.ticket_id} → {final}")

print(f"\nTotal decisions in log: {logger.count()}")
print("Log file: logs/decisions.jsonl")