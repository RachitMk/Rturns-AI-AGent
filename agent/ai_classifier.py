import json
from typing import Dict
from groq import Groq

client = Groq()

SYSTEM_PROMPT = """
You are a returns processing assistant.

Your task is to read a customer return request and extract structured facts.

Rules:
- Output ONLY valid JSON.
- Do NOT include explanations or extra text.
- Do NOT decide refunds or outcomes.
- If information is missing, make a reasonable assumption.

Use this schema exactly:
{
  "return_category": "size_issue | damaged_item | wrong_item | not_as_described | late_delivery | changed_mind | other",
  "condition": "opened | unopened | damaged",
  "packaging_opened": true | false,
  "damage_on_arrival": true | false,
  "late_delivery": true | false
}
"""

def classify_return(text: str) -> Dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content
    return json.loads(raw)
