import json
with open("data/documentation.json") as f:
    docs = json.load(f)
print(f"Total articles: {len(docs)}")
print("Keys in first article:", list(docs[0].keys()))
print(json.dumps(docs[0], indent=2)[:600])