"""Build the FinChat vector store from recent SEC 10-K filings (EDGAR).

Pipeline:
    fetch each target 10-K (edgartools)  ->  split into chunks
    ->  embed locally  ->  store in Chroma (persisted to config.VECTORSTORE_DIR)

Run once, from the project root:
    python -m src.ingest
"""
from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

# Allow running as either `python -m src.ingest` or `python src/ingest.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from edgar import Company, set_identity
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src import config
from src.financials import financial_documents

# Windows consoles default to cp1252 and crash when print() emits Unicode
# (arrows, em-dashes, curly quotes from filings). Force UTF-8 output.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def get_filing(ticker: str, fiscal_year: int):
    """Return the 10-K filing whose fiscal period matches fiscal_year, else None.

    Matches on the filing's period_of_report year, so an offset fiscal year
    (e.g. Amcor's June close) still resolves to the right filing.
    """
    for f in Company(ticker).get_filings(form="10-K"):
        period = getattr(f, "period_of_report", None)
        if period and str(period)[:4] == str(fiscal_year):
            return f
    return None


def fetch_documents() -> list[Document]:
    """Fetch every target filing -> text chunks + structured financial facts."""
    set_identity(config.EDGAR_IDENTITY)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    docs: list[Document] = []
    for ticker, name, year in config.TARGET_FILINGS:
        print(f"Fetching {ticker} FY{year} 10-K ...", end=" ", flush=True)
        filing = get_filing(ticker, year)
        if filing is None:
            print("NOT FOUND -- skipping")
            continue

        # 1) Filing TEXT -> chunks (for qualitative questions).
        text = filing.text()
        source = f"{name} 10-K (FY{year})"
        for chunk in splitter.split_text(text):
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "ticker": ticker,
                        "company": name,
                        "year": str(year),
                        "accession": filing.accession_no,
                        "source": source,
                        "type": "text",
                    },
                )
            )

        # 2) XBRL FINANCIAL STATEMENTS -> structured facts (numeric questions).
        fin_docs = financial_documents(filing, ticker, name, year)
        docs.extend(fin_docs)

        print(f"{len(text):,} chars + {len(fin_docs)} financial statements "
              f"-> {len(docs)} docs so far")
        time.sleep(0.5)   # be polite to SEC's servers
    return docs


def _safe_rmtree(path: Path, retries: int = 3) -> None:
    """Delete a directory, retrying briefly through transient file locks."""
    for _ in range(retries):
        try:
            shutil.rmtree(path)
            return
        except (PermissionError, OSError):
            time.sleep(1.0)
    shutil.rmtree(path)


def build_vectorstore(chunks: list[Document]) -> None:
    if config.VECTORSTORE_DIR.exists():
        print("Removing existing vector store ...")
        _safe_rmtree(config.VECTORSTORE_DIR)
    config.VECTORSTORE_DIR.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model {config.EMBEDDING_MODEL} ...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    print(f"Embedding & storing {len(chunks)} chunks (a few minutes) ...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.CHROMA_COLLECTION,
        persist_directory=str(config.VECTORSTORE_DIR),
    )
    print(f"Done. Vector store saved to: {config.VECTORSTORE_DIR}")


def build_index() -> None:
    """Full pipeline: fetch filings -> chunk -> embed -> store.

    Importable so the app can bootstrap the store on first run.
    """
    docs = fetch_documents()
    if not docs:
        raise SystemExit("No filings were fetched — check tickers/years in config.py.")
    print(f"Total: {len(docs)} chunks from {len(config.TARGET_FILINGS)} target filings.")
    build_vectorstore(docs)


def main() -> None:
    build_index()


if __name__ == "__main__":
    main()
