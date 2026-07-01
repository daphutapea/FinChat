"""Build the FinChat vector store from SEC 10-K filings.

Pipeline:
    load sentences  ->  group into section text  ->  split into chunks
    ->  embed locally  ->  store in Chroma (persisted to ./vectorstore)

Run it once (from the project root):
    python -m src.ingest            # build the vector store
    python -m src.ingest --list     # just list available companies, then exit
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from pathlib import Path

# Allow running as either `python -m src.ingest` or `python src/ingest.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from datasets import load_dataset
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src import config


def pretty_section(label: str) -> str:
    """Turn a raw section label into a readable 'Section N' for display."""
    nums = re.findall(r"\d+", str(label))
    if nums:
        return f"Section {nums[-1]}"
    return str(label).replace("_", " ").strip().title() or "Filing"


def load_dataframe() -> pd.DataFrame:
    """Download the dataset split and return it as a tidy DataFrame."""
    print(f"Loading {config.HF_DATASET} [{config.HF_CONFIG}] ... (first run downloads it)")
    ds = load_dataset(
        config.HF_DATASET, config.HF_CONFIG, split=config.HF_SPLIT,
        trust_remote_code=True,
    )
    df = ds.to_pandas()

    # `tickers` is a list per row -> take the first as the primary ticker.
    df["ticker"] = df["tickers"].apply(
        lambda t: t[0] if hasattr(t, "__len__") and len(t) else None
    )
    # reportDate looks like "2020-09-26"; the year is the first 4 chars.
    df["year"] = df["reportDate"].astype(str).str.slice(0, 4)
    return df


def list_companies(df: pd.DataFrame, top: int = 30) -> None:
    counts = (
        df.dropna(subset=["ticker"])
        .groupby(["ticker", "name"])
        .size()
        .sort_values(ascending=False)
        .head(top)
    )
    print("\nTop companies available (ticker | name | #sentences):")
    for (ticker, name), n in counts.items():
        print(f"  {ticker:<8} {str(name):<42} {n}")
    print("\nCopy the tickers you want into TARGET_TICKERS in src/config.py.")


def select_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["ticker"]).copy()

    if config.TARGET_YEARS:
        years = {str(y) for y in config.TARGET_YEARS}
        df = df[df["year"].isin(years)]

    if config.TARGET_TICKERS:
        wanted = {t.upper() for t in config.TARGET_TICKERS}
        df = df[df["ticker"].str.upper().isin(wanted)]
    else:
        # No explicit list -> keep the TOP_N companies by content volume.
        top = (
            df.groupby("ticker").size()
            .sort_values(ascending=False)
            .head(config.TOP_N_COMPANIES)
            .index
        )
        df = df[df["ticker"].isin(top)]

    return df


def build_documents(df: pd.DataFrame) -> list[Document]:
    """Reassemble sentences into section text, then split into chunks."""
    # One "raw document" per (filing, section). docID identifies one filing.
    grouped = df.sort_values("sentenceCount").groupby(["docID", "section"])

    raw_docs: list[Document] = []
    for (doc_id, section), rows in grouped:
        text = " ".join(str(s) for s in rows["sentence"].tolist()).strip()
        if len(text) < 50:                 # skip near-empty sections
            continue
        head = rows.iloc[0]
        company = str(head["name"])
        year = str(head["year"])
        raw_docs.append(
            Document(
                page_content=text,
                metadata={
                    "ticker": str(head["ticker"]),
                    "company": company,
                    "year": year,
                    "section": str(section),
                    "cik": str(head["cik"]),
                    "docID": str(doc_id),
                    "source": f"{company} 10-K ({year}) - {pretty_section(section)}",
                },
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"Reassembled {len(raw_docs)} sections -> {len(chunks)} chunks.")
    return chunks


def _safe_rmtree(path: Path, retries: int = 3) -> None:
    """Delete a directory, retrying briefly through transient file locks."""
    for _ in range(retries):
        try:
            shutil.rmtree(path)
            return
        except (PermissionError, OSError):
            time.sleep(1.0)
    shutil.rmtree(path)   # last try -- let the error surface if it still fails


def build_vectorstore(chunks: list[Document]) -> None:
    if config.VECTORSTORE_DIR.exists():
        print("Removing existing vector store ...")
        _safe_rmtree(config.VECTORSTORE_DIR)
    config.VECTORSTORE_DIR.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model {config.EMBEDDING_MODEL} ...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    print("Embedding & storing chunks (this can take a few minutes) ...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.CHROMA_COLLECTION,
        persist_directory=str(config.VECTORSTORE_DIR),
    )
    print(f"Done. Vector store saved to: {config.VECTORSTORE_DIR}")


def build_index() -> None:
    """Run the full ingestion pipeline: load -> select -> chunk -> embed -> store.

    Importable so the app can bootstrap the vector store on first run
    (e.g. on a fresh Hugging Face Space).
    """
    df = load_dataframe()
    selected = select_rows(df)
    if selected.empty:
        raise SystemExit(
            "\nNo rows matched TARGET_TICKERS / TARGET_YEARS in src/config.py.\n"
            "Run `python -m src.ingest --list` to see what's available."
        )
    companies = sorted(selected["ticker"].unique())
    print(f"Ingesting {len(companies)} companies: {', '.join(companies)}")
    chunks = build_documents(selected)
    build_vectorstore(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the FinChat vector store.")
    parser.add_argument("--list", action="store_true",
                        help="List available companies and exit.")
    args = parser.parse_args()

    if args.list:
        list_companies(load_dataframe())
        return

    build_index()


if __name__ == "__main__":
    main()
