"""Central configuration for FinChat.

Everything you might want to tune lives here, so you don't have to hunt
through the code. Edit values, then re-run ingestion.
"""
import os
from pathlib import Path

# --- Paths ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

# Keep the vector store OUTSIDE OneDrive. OneDrive syncs files as they're
# written, which locks ChromaDB's SQLite database mid-write on Windows
# (PermissionError / possible corruption). The store is disposable -- it's
# rebuilt by ingest.py -- so its location doesn't matter to the repo.
# Override with the FINCHAT_VECTORSTORE env var (e.g. on Hugging Face Spaces).
VECTORSTORE_DIR = Path(
    os.getenv("FINCHAT_VECTORSTORE", str(Path.home() / ".finchat" / "vectorstore"))
)

# --- Dataset (Hugging Face) -------------------------------------------------
# Each row is ONE sentence from a 10-K filing. ingest.py reassembles the
# sentences into section text before chunking. "small_full" (~240k sentences)
# keeps the download light enough for a laptop.
HF_DATASET = "JanosAudran/financial-reports-sec"
HF_CONFIG = "small_full"
HF_SPLIT = "train"

# --- Corpus scope -----------------------------------------------------------
# Which companies to ingest. Leave TARGET_TICKERS = [] to auto-pick the
# TOP_N_COMPANIES with the most content (handy before you know what's in the
# data -- run `python -m src.ingest --list` to see the options).
# Recognizable companies available in the "small_full" config, recent years.
# Swap freely: also available -> CECE, BKTI, ACU, AE, WDDD (all end at 2020).
TARGET_TICKERS: list[str] = ["AMD", "ABT", "APD", "AIR", "MATX"]
TARGET_YEARS: list[int] = [2017, 2018, 2019, 2020]
TOP_N_COMPANIES = 8                 # used only when TARGET_TICKERS is empty

# --- Chunking ---------------------------------------------------------------
CHUNK_SIZE = 900                    # characters per chunk
CHUNK_OVERLAP = 150                 # overlap keeps sentences from being cut off

# --- Models -----------------------------------------------------------------
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"   # local, free, ~130 MB on first run
LLM_MODEL = "llama-3.3-70b-versatile"        # Groq free tier
LLM_TEMPERATURE = 0.0                         # 0 = factual, deterministic

# --- Retrieval --------------------------------------------------------------
TOP_K = 8                           # how many chunks to feed the LLM

# --- Vector store -----------------------------------------------------------
CHROMA_COLLECTION = "finchat_10k"
