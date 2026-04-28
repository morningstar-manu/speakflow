# SpeakFlow Backend

## Lancement rapide

```bash
cp .env.example .env
# Remplis GROQ_API_KEY avec ta clé https://console.groq.com
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Architecture agents

| Agent | Rôle | Modèle |
|-------|------|--------|
| DebitAgent | Calcule les WPM, détecte rythme trop lent/rapide | Local (comptage) |
| ParasitesAgent | Détecte "euh", "voilà", "donc"... | Regex local |
| SentimentAgent | Confiance, assertivité, hésitation | Groq LLaMA 3.3 70B |
| LangueAgent | Correction grammaticale, reformulation | Groq LLaMA 3.3 70B |

## WebSocket

```
ws://localhost:8000/stream/ws/{session_id}?language=fr
```

Envoie des chunks audio (WebM/16kHz), reçoit du JSON :

```json
{
  "type": "feedback",
  "chunk": "texte transcrit",
  "agents": {
    "debit": {"wpm": 145, "status": "ok"},
    "parasites": {"fillers": ["euh"], "count": 1},
    "sentiment": {"label": "confident", "confidence": 0.82},
    "langue": {"suggestion": "Reformule ainsi : ..."}
  },
  "feedback": "Bonne fluidité — continue ainsi.",
  "elapsed": 12.4
}
```

## Roadmap

- [ ] Remplacer le store in-memory par PostgreSQL
- [ ] Ajouter l'Agent Mémoire (stats de progression hebdomadaire)
- [ ] Mode Jeu : sujets générés par LLM, leaderboard
- [ ] Export session en PDF avec transcript annoté
