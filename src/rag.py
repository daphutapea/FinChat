"""FinChat retrieval-augmented generation (RAG) chain.

Public entry point:  answer(question) -> {"answer", "routed_to", "sources"}
"""
from __future__ import annotations

import os
import re
from collections import defaultdict
from functools import lru_cache

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src import config

# Load GROQ_API_KEY from the project's .env by explicit path (robust no matter
# where the process is launched). On Hugging Face Spaces there is no .env and
# this is a harmless no-op -- the key comes from Space secrets instead.
load_dotenv(config.PROJECT_ROOT / ".env")

SYSTEM_PROMPT = """You are FinChat, a financial analyst assistant. Answer the \
question using ONLY the excerpts from SEC 10-K filings provided below.

Rules:
- Use ONLY the provided context. Do NOT rely on outside knowledge.
- If the answer is not in the context, reply exactly:
  "I couldn't find that in the filings I have."
- Be concise and precise with numbers. State the company and fiscal year.
- End with a short "Sources:" list referencing the excerpts you used.

Context:
{context}
"""

PROMPT = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", "{question}")]
)


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    return Chroma(
        collection_name=config.CHROMA_COLLECTION,
        embedding_function=embeddings,
        persist_directory=str(config.VECTORSTORE_DIR),
    )


def ensure_index() -> None:
    """Build the vector store on first run if it's empty or missing.

    Lets the app bootstrap itself on a fresh deployment (e.g. Hugging Face
    Spaces). On normal runs where the store already exists, this is a fast
    no-op.
    """
    try:
        has_docs = len(get_vectorstore().get(limit=1).get("ids", [])) > 0
    except Exception:
        has_docs = False
    if not has_docs:
        get_vectorstore.cache_clear()          # release the empty store handle
        from src.ingest import build_index
        build_index()
        get_vectorstore.cache_clear()           # reopen the freshly built store


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")
    return ChatGroq(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        max_retries=5,   # back off through Groq free-tier rate limits
    )


# Words that shouldn't count as a company alias on their own.
_STOPWORDS = {
    "inc", "corp", "corporation", "company", "ltd", "llc", "plc", "the",
    "and", "group", "holdings", "international", "industries", "products",
    "resources", "energy", "technologies", "systems",
}


@lru_cache(maxsize=1)
def company_aliases() -> dict[str, str]:
    """Map each recognizable alias (ticker or distinctive name word) -> ticker.

    This lets FinChat route a question to the right company before retrieving
    ("knows exactly where to look"). Any alias shared by more than one company
    is dropped, so we never route to the wrong filing.
    """
    store = get_vectorstore()
    metadatas = store.get(include=["metadatas"]).get("metadatas", [])

    ticker_to_name: dict[str, str] = {}
    for m in metadatas:
        ticker = (m.get("ticker") or "").upper()
        if ticker:
            ticker_to_name[ticker] = m.get("company") or ""

    alias_to_tickers: dict[str, set] = defaultdict(set)
    for ticker, name in ticker_to_name.items():
        alias_to_tickers[ticker.lower()].add(ticker)          # the ticker itself
        for word in re.findall(r"[a-z]+", name.lower()):
            if len(word) >= 4 and word not in _STOPWORDS:
                alias_to_tickers[word].add(ticker)

    # Keep only unambiguous aliases (mapping to exactly one company).
    return {a: next(iter(ts)) for a, ts in alias_to_tickers.items() if len(ts) == 1}


@lru_cache(maxsize=1)
def available_companies() -> list[tuple[str, str]]:
    """Return sorted (ticker, company name) pairs present in the vector store."""
    store = get_vectorstore()
    metadatas = store.get(include=["metadatas"]).get("metadatas", [])
    seen: dict[str, str] = {}
    for m in metadatas:
        ticker = (m.get("ticker") or "").upper()
        if ticker and ticker not in seen:
            seen[ticker] = m.get("company") or ticker
    return sorted(seen.items())


def detect_ticker(question: str) -> str | None:
    """Figure out which company the question is about."""
    aliases = company_aliases()

    # 1) An explicit ticker written in capitals, e.g. "AMD" or "ABT".
    for token in re.findall(r"\b[A-Z]{2,6}\b", question):
        if token.lower() in aliases:
            return aliases[token.lower()]

    # 2) A distinctive company-name word, e.g. "abbott" or "matson".
    for word in re.findall(r"[a-z]+", question.lower()):
        if len(word) >= 4 and word in aliases:
            return aliases[word]

    return None


def retrieve(question: str, ticker: str | None):
    store = get_vectorstore()
    search_kwargs: dict = {"k": config.TOP_K}
    if ticker:
        # Metadata filter = search ONLY that company's filings.
        search_kwargs["filter"] = {"ticker": ticker}
    return store.as_retriever(search_kwargs=search_kwargs).invoke(question)


def format_context(docs) -> str:
    return "\n\n".join(
        f"[{i}] {d.metadata.get('source', 'source')}\n{d.page_content}"
        for i, d in enumerate(docs, 1)
    )


def answer(question: str) -> dict:
    """Route -> retrieve -> generate. Returns answer, routing info, sources."""
    ticker = detect_ticker(question)
    docs = retrieve(question, ticker)
    context = format_context(docs) if docs else "(no relevant excerpts found)"
    chain = PROMPT | get_llm()
    response = chain.invoke({"context": context, "question": question})
    return {"answer": response.content, "routed_to": ticker, "sources": docs}
