from src.data_loader import load_tickets, channel_counts

tickets = load_tickets("data/development_tickets.json")

print(f"Total tickets loaded: {len(tickets)}")
print("Channel counts:", channel_counts(tickets))

# Show one sample from each channel
seen = set()
for t in tickets:
    if t.channel not in seen:
        print(f"\n--- Sample from channel: {t.channel} ---")
        print(f"ID: {t.ticket_id}")
        print(f"Subject: {t.subject[:80]}")
        print(f"Intent (label): {t.labels.intent}")
        print(f"Urgency (label): {t.labels.urgency}")
        seen.add(t.channel)
    if len(seen) == 4:
        break

print("\nData loading and normalisation OK")