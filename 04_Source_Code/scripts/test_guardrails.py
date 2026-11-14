from src.data_loader import load_tickets
from src.guardrails import Guardrails

tickets = load_tickets("data/development_tickets.json")
guard = Guardrails()

# Test 1: tickets that should be blocked by flag
blocked = [t for t in tickets if t.labels.must_not_auto_respond is True][:2]
for t in blocked:
    result = guard.check(t)
    print(f"{t.ticket_id} | must_not={t.labels.must_not_auto_respond} → {result}")

# Test 2: normal ticket
normal = next(t for t in tickets if t.labels.must_not_auto_respond is not True)
print(f"\n{normal.ticket_id} | normal → {guard.check(normal)}")

# Test 3: simulated bad answer
fake_generated = {"answer": "Please use password: secret123 and email admin@company.com", "confidence": 0.9}
print(f"\nFake bad answer → {guard.check(normal, fake_generated)}")