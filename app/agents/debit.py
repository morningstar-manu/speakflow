class DebitAgent:
    SLOW_THRESHOLD = 100
    FAST_THRESHOLD = 180

    async def analyze(self, transcript: str, elapsed_seconds: float) -> dict:
        words = [w for w in transcript.split() if w.strip()]
        if elapsed_seconds <= 0:
            return {"wpm": None, "status": "ok"}
        wpm = int(len(words) / (elapsed_seconds / 60))
        status = "slow" if wpm < self.SLOW_THRESHOLD else "fast" if wpm > self.FAST_THRESHOLD else "ok"
        return {"wpm": wpm, "status": status, "word_count": len(words)}
