from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

router = APIRouter()
sessions_db: dict = {}

class SessionCreate(BaseModel):
    subject: Optional[str] = None
    mode: str = "libre"
    language: str = "fr"

class SessionResult(BaseModel):
    session_id: str
    wpm_avg: Optional[int] = None
    filler_count: int = 0
    fluency_score: Optional[float] = None
    duration_seconds: int = 0
    transcript: Optional[str] = None

@router.post("/")
def create_session(body: SessionCreate):
    sid = str(uuid.uuid4())
    sessions_db[sid] = {"id": sid, "subject": body.subject, "mode": body.mode,
                        "language": body.language, "created_at": datetime.utcnow().isoformat(), "results": None}
    return {"session_id": sid}

@router.post("/{session_id}/result")
def save_result(session_id: str, result: SessionResult):
    if session_id not in sessions_db:
        return {"error": "session not found"}
    sessions_db[session_id]["results"] = result.dict()
    return {"ok": True}

@router.get("/{session_id}")
def get_session(session_id: str):
    return sessions_db.get(session_id, {"error": "not found"})

@router.get("/")
def list_sessions():
    return list(sessions_db.values())
