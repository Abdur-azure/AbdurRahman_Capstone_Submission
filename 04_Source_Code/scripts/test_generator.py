from src.data_loader import load_tickets
from src.classifier import TicketClassifier
from src.retriever import DocumentRetriever
from src.router import Router
from src.generator import AnswerGenerator

tickets = load_tickets("data/development_tickets.json")
classifier = TicketClassifier()
retriever = DocumentRetriever()
retriever.build_index()
router = Router(confidence_threshold=0.65)
generator = AnswerGenerator()

# Find a few tickets that are likely to be answerable
for t in tickets[:10]:
    classification = classifier.classify(t)
    query = f"{t.subject} {t.body[:300]}"
    docs = retriever.retrieve(query, top_k=3)
    decision = router.decide(t, classification, docs)

    if decision["decision"] != "answer":
        continue

    result = generator.generate(t, docs)
    print(f"\n=== {t.ticket_id} ===")
    print(f"Decision: {decision['decision']}")
    print(f"Answer:\n{result['answer'][:400]}")
    print(f"Citations: {result['citations']}")
    print(f"Confidence: {result['confidence']:.2f}")
    break   # just show one successful example for now