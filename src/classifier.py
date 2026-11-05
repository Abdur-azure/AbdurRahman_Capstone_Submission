import os
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from src.models import Ticket

load_dotenv()

class TicketClassifier:
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        """
        Uses Groq (or OpenRouter) free-tier model.
        Change model name if you are using a different free model.
        """
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),          # or OPENROUTER_API_KEY
            base_url="https://api.groq.com/openai/v1"  # change for OpenRouter
        )
        self.model = model

        self.system_prompt = """You are a support ticket classifier for CloudServe Solutions.
Given the ticket subject and body, classify:
1. intent – the most specific technical category
2. urgency – high, medium or low
3. confidence – a number between 0.0 and 1.0

Return ONLY valid JSON with the keys: intent, urgency, confidence.
Do not invent information that is not present in the ticket."""

    def classify(self, ticket: Ticket) -> Dict[str, Any]:
        user_content = f"Subject: {ticket.subject}\n\nBody: {ticket.body}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.0,
            max_tokens=150
        )

        raw = response.choices[0].message.content.strip()

        # Clean possible markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback if model returns bad JSON
            result = {
                "intent": "unclear_request",
                "urgency": "medium",
                "confidence": 0.3
            }

        # Basic validation
        result["confidence"] = float(result.get("confidence", 0.5))
        result["confidence"] = max(0.0, min(1.0, result["confidence"]))
        if result.get("urgency") not in ("high", "medium", "low"):
            result["urgency"] = "medium"

        return result