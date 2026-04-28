import os, json
from groq import AsyncGroq

SYSTEM = """Analyse ce texte oral et retourne UNIQUEMENT ce JSON :
{"label":"confident|neutral|hesitant|assertive|anxious","confidence":0.0-1.0,"tone":"string","suggestion":null}"""

class SentimentAgent:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    async def analyze(self, transcript: str) -> dict:
        if len(transcript.split()) < 5:
            return {"label": "neutral", "confidence": 0.5, "tone": "en attente"}
        try:
            r = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"system","content":SYSTEM},{"role":"user","content":transcript}],
                max_tokens=150, temperature=0.2,
            )
            return json.loads(r.choices[0].message.content.strip())
        except Exception as e:
            return {"label": "neutral", "confidence": 0.5, "error": str(e)}
