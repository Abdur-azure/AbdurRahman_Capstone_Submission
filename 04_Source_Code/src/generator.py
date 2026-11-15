import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from src.models import Ticket
from src.config import require_api_key, MODEL_NAME

load_dotenv()

class AnswerGenerator:
    def __init__(self, model: str = MODEL_NAME):
        self.client = OpenAI(
            api_key=require_api_key(),          # or OPENROUTER_API_KEY
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = model

        self.system_prompt = """You are a CloudServe support assistant.
        Answer the customer ticket using ONLY the provided documentation passages.
        
        Rules:
        - Prefer giving a useful answer when the passages contain relevant information.
        - Only say you cannot answer if the passages are clearly irrelevant or empty.
        - Every factual claim must be supported by a citation to one of the passage IDs.
        - Be clear, professional and concise.
        - Return ONLY valid JSON with keys: answer, citations (list of doc_ids), confidence (0.0-1.0).
        """

    def generate(
        self,
        ticket: Ticket,
        retrieved_docs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Build context from retrieved passages
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(
                f"[{doc['doc_id']}] {doc['title']}\n{doc['text']}"
            )
        context = "\n\n".join(context_parts)

        user_content = f"""Customer ticket:
        Subject: {ticket.subject}
        Body: {ticket.body}

        Documentation passages:
        {context}

        Generate the answer now."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            max_tokens=500
        )

        raw = response.choices[0].message.content.strip()

        # Clean markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            result = {
                "answer": "I was unable to generate a reliable answer from the available documentation. Please escalate to a human agent.",
                "citations": [],
                "confidence": 0.2
            }

        # Ensure citations only contain real retrieved doc_ids
        valid_ids = {d["doc_id"] for d in retrieved_docs}
        citations = result.get("citations", [])
        result["citations"] = [c for c in citations if c in valid_ids]

        result["confidence"] = float(result.get("confidence", 0.5))
        result["confidence"] = max(0.0, min(1.0, result["confidence"]))

        return result