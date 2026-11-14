from src.data_loader import load_tickets
from src.classifier import TicketClassifier
from src.retriever import DocumentRetriever
from src.router import Router

tickets = load_tickets("data/development_tickets.json")
classifier = TicketClassifier()
retriever = DocumentRetriever()
retriever.build_index()          # safe if already built
router = Router(confidence_threshold=0.65)

for t in tickets[:5]:
    classification = classifier.classify(t)
    query = f"{t.subject} {t.body[:300]}"
    docs = retriever.retrieve(query, top_k=3)
    decision = router.decide(t, classification, docs)

    print(f"{t.ticket_id} | conf={classification['confidence']:.2f} | docs={len(docs)} | → {decision['decision']} ({decision['reason']})")