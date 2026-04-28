from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import sessions, stream

app = FastAPI(title="SpeakFlow API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(stream.router, prefix="/stream", tags=["stream"])

@app.get("/health")
def health(): return {"status": "ok"}
