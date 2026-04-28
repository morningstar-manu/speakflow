import re

FILLERS = {
    "fr": ["euh", "heu", "voila", "voilà", "donc", "en fait", "genre", "bah", "du coup", "enfin", "bon", "ouais", "hm"],
    "en": ["um", "uh", "like", "you know", "basically", "literally", "right", "so", "actually", "I mean"],
}

class ParasitesAgent:
    def __init__(self, language: str = "fr"):
        self.fillers = FILLERS.get(language, FILLERS["fr"])

    async def analyze(self, transcript: str) -> dict:
        lower = transcript.lower()
        found = []
        for f in self.fillers:
            matches = re.findall(r'\b' + re.escape(f) + r'\b', lower)
            found.extend(matches)
        return {"fillers": found, "count": len(found), "types": list(set(found))}
