import os, json
from groq import AsyncGroq

PROMPTS = {
    "fr": 'Analyse ce discours oral. Retourne UNIQUEMENT: {"grammar_errors":[],"suggestion":"reformulation max 20 mots ou null","register":"formal|informal|neutral"}',
    "en": 'Analyze this spoken text. Return ONLY: {"grammar_errors":[],"suggestion":"rephrasing max 20 words or null","register":"formal|informal|neutral"}',
}

class LangueAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    async def analyze(self, transcript: str, session_context: str = "") -> dict:
        if len(transcript.split()) < 8:
            return {"suggestion": None, "grammar_errors": []}
        try:
            r = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"system","content":PROMPTS.get(self.language,PROMPTS["fr"])},{"role":"user","content":transcript}],
                max_tokens=200, temperature=0.3,
            )
            return json.loads(r.choices[0].message.content.strip())
        except Exception as e:
            return {"suggestion": None, "error": str(e)}
