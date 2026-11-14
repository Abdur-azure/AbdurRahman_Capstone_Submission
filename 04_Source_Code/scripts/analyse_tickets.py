import json
from collections import Counter

with open("../data/development_tickets.json") as f:   # adjust path if needed
    tickets = json.load(f)

print(f"Total tickets: {len(tickets)}")

# Channel split
channels = Counter(t["channel"] for t in tickets)
print("\nBy channel:")
for k, v in channels.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Intent split
intents = Counter(t["labels"]["intent"] for t in tickets)
print("\nBy intent:")
for k, v in intents.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Urgency split
urgency = Counter(t["labels"]["urgency"] for t in tickets)
print("\nBy urgency:")
for k, v in urgency.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Language fluency
fluency = Counter(t.get("language_fluency", "unknown") for t in tickets)
print("\nBy language_fluency:")
for k, v in fluency.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Customer tier
tiers = Counter(t.get("customer_tier", "unknown") for t in tickets)
print("\nBy customer_tier:")
for k, v in tiers.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Expected route (useful for escalation / FCR proxy)
routes = Counter(t["labels"].get("expected_route", "unknown") for t in tickets)
print("\nBy expected_route:")
for k, v in routes.most_common():
    print(f"  {k}: {v} ({v/len(tickets)*100:.1f}%)")

# Proportion marked resolved on first contact
fcr_true = sum(1 for t in tickets if t["history"].get("first_contact_resolution") is True)
fcr_pct = fcr_true / len(tickets) * 100
print(f"\nFirst Contact Resolution: {fcr_true}/{len(tickets)} = {fcr_pct:.1f}%")

# Average satisfaction rating (CSAT)
csat_scores = [t["history"]["csat_rating"] for t in tickets if t["history"].get("csat_rating") is not None]
avg_csat = sum(csat_scores) / len(csat_scores)
print(f"Average CSAT: {avg_csat:.2f} (from {len(csat_scores)} tickets)")
print("CSAT distribution:", Counter(csat_scores))

# Most frequent single question / intent
from collections import Counter
intents = Counter(t["labels"]["intent"] for t in tickets)
print("\nMost frequent intents:")
for intent, count in intents.most_common(5):
    print(f"  {intent}: {count} ({count/len(tickets)*100:.1f}%)")

# Proportion answerable from existing documentation
answerable = sum(1 for t in tickets if t["labels"].get("answerable_from_docs") is True)
answerable_pct = answerable / len(tickets) * 100
print(f"\nAnswerable from docs: {answerable}/{len(tickets)} = {answerable_pct:.1f}%")

# Proportion that are repeat contacts
repeat_true = sum(1 for t in tickets if t["history"].get("repeat_contact") is True)
repeat_pct = repeat_true / len(tickets) * 100
print(f"\nRepeat contacts: {repeat_true}/{len(tickets)} = {repeat_pct:.1f}%")