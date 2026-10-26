import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB = Path(__file__).with_name("mindful_minute.db")
app = FastAPI(title="Mindful Minute — Coursework Prototype")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def now():
    return datetime.now(timezone.utc).isoformat()

def connection():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

@app.on_event("startup")
def setup():
    with connection() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT NOT NULL, started_at TEXT NOT NULL, ended_at TEXT,
            guided_seconds INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'active')""")
        db.execute("""CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL)""")
        db.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id))""")

class SessionFinish(BaseModel):
    status: Literal["completed", "interrupted"]
    guided_seconds: int = Field(ge=0, le=90)

class ChatInput(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    conversation_id: int | None = None

@app.get("/api/health")
def health():
    return {"status": "ok", "prototype": True}

@app.post("/api/sessions")
def start_session():
    with connection() as db:
        cur = db.execute("INSERT INTO sessions(skill, started_at) VALUES (?, ?)", ("4-6 breathing", now()))
        return {"id": cur.lastrowid, "status": "active"}

@app.patch("/api/sessions/{session_id}")
def finish_session(session_id: int, body: SessionFinish):
    with connection() as db:
        row = db.execute("SELECT status FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Session not found")
        if row["status"] != "active":
            raise HTTPException(409, "Session already finished")
        db.execute("UPDATE sessions SET status=?, guided_seconds=?, ended_at=? WHERE id=?",
                   (body.status, body.guided_seconds, now(), session_id))
    return {"id": session_id, "status": body.status}

@app.get("/api/sessions")
def sessions():
    with connection() as db:
        return [dict(row) for row in db.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT 50")]

@app.get("/api/sessions/{session_id}")
def session_detail(session_id: int):
    with connection() as db:
        row = db.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Session not found")
        return dict(row)

@app.get("/api/conversations/{conversation_id}")
def conversation_detail(conversation_id: int):
    with connection() as db:
        messages = db.execute("SELECT role, content, created_at FROM messages WHERE conversation_id=? ORDER BY id", (conversation_id,)).fetchall()
        return [dict(m) for m in messages]

@app.post("/api/chat")
def chat(body: ChatInput):
    # The model only offers brief, optional explanations; never controls safety or breathing timing.
    with connection() as db:
        if body.conversation_id is None:
            cid = db.execute("INSERT INTO conversations(created_at) VALUES (?)", (now(),)).lastrowid
        else:
            cid = body.conversation_id
            if not db.execute("SELECT id FROM conversations WHERE id=?", (cid,)).fetchone():
                raise HTTPException(404, "Conversation not found")
        db.execute("INSERT INTO messages(conversation_id, role, content, created_at) VALUES (?,?,?,?)",
                   (cid, "user", body.message, now()))
        history = db.execute("SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT 8", (cid,)).fetchall()
        history = [dict(m) for m in reversed(history)]
        if not (os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")):
            reply = "Live AI is not configured. You can choose the 60-second 4–6 breathing exercise without using chat."
            mode = "fallback"
        else:
            try:
                from openai import OpenAI
                use_openrouter = bool(os.getenv("OPENROUTER_API_KEY"))
                client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY") if use_openrouter else os.getenv("OPENAI_API_KEY"),
                                base_url="https://openrouter.ai/api/v1" if use_openrouter else "https://api.openai.com/v1", timeout=20)
                response = client.chat.completions.create(
                    model=os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-super-vl:free") if use_openrouter else os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[{"role": "system", "content":
                        "You are an optional interface assistant for a fictional coursework prototype. "
                        "Keep replies under 55 words, calm and neutral. Do not diagnose, provide therapy, "
                        "invent skill steps, claim monitoring, or promise safety. Offer the fixed 4-second "
                        "inhale, 6-second exhale exercise as an optional choice. "
                        "For crisis-related text, encourage immediate human support and the always-visible "
                        "Crisis Support button; do not treat chat as crisis support."}, *history],
                    max_tokens=900,
                    extra_body={"reasoning": {"effort": "none"}} if use_openrouter else {})
                reply = (response.choices[0].message.content or "").strip()
                if not reply:
                    reply = "The model returned an empty answer. Please try again or use the breathing exercise directly."
                    mode = "error"
                else:
                    mode = "live"
            except Exception:
                reply = "The AI chat is unavailable. The breathing exercise and Crisis Support button still work."
                mode = "error"
        db.execute("INSERT INTO messages(conversation_id, role, content, created_at) VALUES (?,?,?,?)",
                   (cid, "assistant", reply, now()))
        return {"conversation_id": cid, "reply": reply, "mode": mode}
