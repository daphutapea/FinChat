"""FinChat HTTP API (FastAPI).

A thin, headless wrapper around the existing RAG engine in ``src/rag.py``.
This is what the Vercel front-end calls. It exposes:

    GET  /            -> service banner
    GET  /health      -> liveness probe
    GET  /companies   -> [{ticker, name}, ...] loaded in the corpus
    POST /chat        -> {answer, routed_to, sources[]}
    GET  /docs        -> interactive Swagger UI (FastAPI built-in)

Run locally from the repo root:
    uvicorn api.main:app --reload --port 7860
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag import answer, available_companies, get_vectorstore


# --- request / response models ---------------------------------------------
class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    index: int
    source: str
    ticker: str | None = None
    company: str | None = None
    type: str | None = None
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    routed_to: str | None = None
    sources: list[Source]


# --- lifespan: warm the model once at boot ---------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the vector store + embedding model a single time at startup, so the
    # first real user request doesn't pay the cold-load cost.
    get_vectorstore()
    yield


app = FastAPI(title="FinChat API", version="1.0.0", lifespan=lifespan)

# Allow the Vercel front-end (and localhost during development) to call us.
# Set FRONTEND_ORIGIN in the Space secrets to your Vercel URL(s), comma-separated.
_origins = [o.strip() for o in os.getenv("FRONTEND_ORIGIN", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins or ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Optional shared secret. If API_SECRET is set (as a Space secret), callers must
# send it as the "X-API-Key" header. The Vercel proxy adds it automatically, so
# random traffic can't hit this Space directly and burn the Groq daily quota.
_API_SECRET = os.getenv("API_SECRET")


def _check_auth(x_api_key: str | None) -> None:
    if _API_SECRET and x_api_key != _API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


@app.get("/")
def root():
    return {"service": "FinChat API", "status": "ok", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/companies")
def companies():
    return [{"ticker": t, "name": n} for t, n in available_companies()]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, x_api_key: str | None = Header(default=None)):
    _check_auth(x_api_key)
    question = (req.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="question must not be empty.")

    result = answer(question)
    sources = [
        Source(
            index=i,
            source=d.metadata.get("source", ""),
            ticker=d.metadata.get("ticker"),
            company=d.metadata.get("company"),
            type=d.metadata.get("type"),
            excerpt=d.page_content[:500],
        )
        for i, d in enumerate(result["sources"], 1)
    ]
    return ChatResponse(
        answer=result["answer"],
        routed_to=result["routed_to"],
        sources=sources,
    )
