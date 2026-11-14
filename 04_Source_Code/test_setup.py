import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()

print("1. Testing embeddings (local)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
emb = embedder.encode(["CloudServe support ticket test"])
print(f"   Embedding shape: {emb.shape} → OK")

print("\n2. Testing LLM connection...")
# --- Use the provider you set up ---
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),               # or OPENROUTER_API_KEY
    base_url="https://api.groq.com/openai/v1"        # change if using OpenRouter
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",                      # or another free model you have access to
    messages=[{"role": "user", "content": "Reply with exactly: Setup successful"}],
    max_tokens=20
)
print(f"   LLM reply: {response.choices[0].message.content}")
print("\nAll checks passed.")