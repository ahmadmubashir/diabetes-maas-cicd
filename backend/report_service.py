# backend/report_service.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from typing import List

# Load .env from project root (two levels up from this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def generate_gpt_report(
    prediction: str,
    probability: float,
    risk_level: str,
    risk_factors: List[str],
    evidence: str
) -> str:
    # (keep the same robust implementation as before)
    # Only change: the .env loading at top
    if not isinstance(probability, (int, float)) or not (0 <= probability <= 1):
        return "[ERROR] Probability must be a float between 0 and 1."
    if not isinstance(risk_factors, list):
        return "[ERROR] risk_factors must be a list of strings."
    if not prediction or not risk_level:
        return "[ERROR] Prediction and risk_level cannot be empty."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set")
        return "[ERROR] OpenAI API key not configured."

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        return f"[ERROR] OpenAI init error: {str(e)}"

    risk_factors_str = ", ".join(risk_factors) if risk_factors else "None reported"
    evidence_text = evidence.strip() if evidence else "No specific guidelines retrieved."

    prompt = f"""
You are a diabetes clinical assistant.

Evidence:
{evidence_text}

Prediction: {prediction}
Probability: {probability:.2%}
Risk Level: {risk_level}
Risk Factors: {risk_factors_str}

INSTRUCTIONS:
- If evidence is insufficient, explicitly state uncertainty.
- Do not fabricate recommendations.
- Do not diagnose.
- Use only evidence-based guidance.

Generate a structured report:

1. Clinical Summary
2. Explanation of Risk
3. Lifestyle Recommendations
4. Monitoring Plan
5. Evidence Sources
6. Disclaimer
"""
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": "You are an evidence-based clinical assistant."},
                    {"role": "user", "content": prompt}
                ],
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                return f"[ERROR] Report generation failed: {str(e)}"
    return "[ERROR] Unexpected execution path."