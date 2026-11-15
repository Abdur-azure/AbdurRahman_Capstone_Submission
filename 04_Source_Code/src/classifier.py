import os
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from src.models import Ticket
from src.config import require_api_key, MODEL_NAME

load_dotenv()

class TicketClassifier:
    def __init__(self, model: str = MODEL_NAME):
        """
        Uses Groq (or OpenRouter) free-tier model.
        Change model name if you are using a different free model.
        """
        self.client = OpenAI(
            api_key=require_api_key(),          # or OPENROUTER_API_KEY
            base_url="https://api.groq.com/openai/v1"  # change for OpenRouter
        )
        self.model = model

        self.system_prompt = """You are a support ticket classifier for CloudServe Solutions.
        
        Classify the ticket into exactly one intent from this list:
        - data_export
        - data_residency
        - rollback_request
        - deployment_failure
        - compliance_request
        - sso_configuration
        - security_incident
        - database_issue
        - api_usage_question
        - billing_query
        - performance_degradation
        - quota_or_overage
        - account_access
        - onboarding
        - integration_help
        - webhook_issue
        - feature_request
        - authentication_failure
        - api_key_issue
        - configuration_help
        - rate_limit
        - unclear_request
        
        Also classify urgency as: high, medium, or low.
        Give a confidence score between 0.0 and 1.0.
        
        Rules:
        - Prefer a specific technical intent over "unclear_request" whenever there is any reasonable signal.
        - Only use "unclear_request" when the ticket is truly impossible to categorise.
        - Return ONLY valid JSON with keys: intent, urgency, confidence.
        """

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