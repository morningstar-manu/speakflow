import asyncio, json, time, io, os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from groq import AsyncGroq
from app.agents.orchestrator import Orchestrator

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_stream(websocket: WebSocket, session_id: str, language: str = "fr"):
    await websocket.accept()
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    orchestrator = Orchestrator(language=language)
    session_transcript = ""
    start_time = time.time()
    audio_buffer = bytearray()

    try:
        while True:
            data = await asyncio.wait_for(websocket.receive_bytes(), timeout=30.0)
            audio_buffer.extend(data)
            if len(audio_buffer) < 48_000:
                continue
            chunk = bytes(audio_buffer)
            audio_buffer.clear()
            elapsed = time.time() - start_time

            try:
                transcription = await client.audio.transcriptions.create(
                    file=("chunk.webm", io.BytesIO(chunk), "audio/webm"),
                    model="whisper-large-v3-turbo",
                    language=language,
                    response_format="text",
                )
                chunk_text = transcription.strip()
            except Exception as e:
                await websocket.send_json({"type": "error", "message": str(e)})
                continue

            if not chunk_text:
                continue

            session_transcript += " " + chunk_text
            result = await orchestrator.process_chunk(
                transcript=session_transcript,
                elapsed_seconds=elapsed,
                session_transcript=session_transcript,
            )
            await websocket.send_json({
                "type": "feedback",
                "chunk": chunk_text,
                "agents": {
                    "debit": {"wpm": result.wpm, "status": result.debit_status},
                    "parasites": {"fillers": result.fillers, "count": result.filler_count},
                    "sentiment": {"label": result.sentiment, "confidence": result.confidence},
                    "langue": {"suggestion": result.language_feedback},
                },
                "feedback": result.feedback_message,
                "elapsed": round(elapsed, 1),
            })
    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        await websocket.send_json({"type": "timeout"})
        await websocket.close()
