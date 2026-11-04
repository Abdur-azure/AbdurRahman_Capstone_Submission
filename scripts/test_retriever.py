from src.retriever import DocumentRetriever

retriever = DocumentRetriever()
retriever.build_index(force_rebuild=True)   # first time

# Test query
results = retriever.retrieve("login fails with invalid credentials", top_k=3)

print(f"Retrieved {len(results)} passages:\n")
for i, r in enumerate(results, 1):
    print(f"{i}. [{r['doc_id']}] {r['title']}")
    print(f"   Distance: {r['distance']:.3f}")
    print(f"   Text: {r['text'][:200]}...\n")