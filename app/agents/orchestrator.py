import asyncio
from dataclasses import dataclass, field
from typing import Optional
from .debit import DebitAgent
from .parasites import ParasitesAgent
from .sentiment import SentimentAgent
from .langue import LangueAgent

@dataclass
class AgentResult:
    wpm: Optional[int] = None
    debit_status: str = "ok"
    fillers: list = field(default_factory=list)
    filler_count: int = 0
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    language_feedback: Optional[str] = None
    feedback_message: str = ""
    transcript_chunk: str = ""

class Orchestrator:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.debit = DebitAgent()
        self.parasites = ParasitesAgent(language)
        self.sentiment = SentimentAgent()
        self.langue = LangueAgent(language)

    async def process_chunk(self, transcript: str, elapsed_seconds: float, session_transcript: str = "") -> AgentResult:
        results = await asyncio.gather(
            self.debit.analyze(transcript, elapsed_seconds),
            self.parasites.analyze(transcript),
            self.sentiment.analyze(transcript),
            self.langue.analyze(transcript, session_transcript),
            return_exceptions=True
        )
        debit_r, parasites_r, sentiment_r, langue_r = results
        result = AgentResult(transcript_chunk=transcript)
        if not isinstance(debit_r, Exception):
            result.wpm = debit_r.get("wpm")
            result.debit_status = debit_r.get("status", "ok")
        if not isinstance(parasites_r, Exception):
            result.fillers = parasites_r.get("fillers", [])
            result.filler_count = parasites_r.get("count", 0)
        if not isinstance(sentiment_r, Exception):
            result.sentiment = sentiment_r.get("label")
            result.confidence = sentiment_r.get("confidence")
        if not isinstance(langue_r, Exception):
            result.language_feedback = langue_r.get("suggestion")
        result.feedback_message = self._build_feedback(result)
        return result

    def _build_feedback(self, r: AgentResult) -> str:
        if r.debit_status == "fast":
            return "Ralentis — tu parles trop vite."
        if r.debit_status == "slow":
            return "Accélère légèrement — engage davantage."
        if r.filler_count >= 3:
            return f'{r.filler_count} hésitations — remplace-les par une pause.'
        if r.sentiment == "hesitant":
            return "Ton ton est hésitant — affirme tes phrases."
        if r.language_feedback:
            return r.language_feedback
        return "Bonne fluidité — continue ainsi."
