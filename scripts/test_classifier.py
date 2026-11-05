from src.data_loader import load_tickets
from src.classifier import TicketClassifier

tickets = load_tickets("data/development_tickets.json")
classifier = TicketClassifier()

# Test on 3 sample tickets
for t in tickets[:3]:
    result = classifier.classify(t)
    print(f"Ticket: {t.ticket_id} | Channel: {t.channel}")
    print(f"  Label intent : {t.labels.intent}")
    print(f"  Pred  intent : {result['intent']}")
    print(f"  Pred  urgency: {result['urgency']} (conf={result['confidence']:.2f})")
    print()