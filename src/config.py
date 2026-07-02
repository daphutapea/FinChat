"""Central configuration for FinChat.

Everything you might want to tune lives here, so you don't have to hunt
through the code. Edit values, then re-run ingestion.
"""
import os
from pathlib import Path

# --- Paths ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

# Where ChromaDB persists the index. The store is disposable -- it's rebuilt
# by ingest.py -- so its location doesn't matter to the repo. Requirements:
#   - Windows: keep it OUTSIDE OneDrive (OneDrive syncs files mid-write and
#     locks ChromaDB's SQLite database) -> use the user's home dir.
#   - Linux containers (e.g. Hugging Face Spaces): the home dir may not be
#     writable, which makes chromadb's storage engine fail to start -> use
#     /tmp, which is writable in any container.
# Override either default with the FINCHAT_VECTORSTORE env var.
_repo_store = PROJECT_ROOT / "vectorstore"      # prebuilt index committed to repo
_default_store = (
    Path.home() / ".finchat" / "vectorstore"
    if os.name == "nt"
    else Path("/tmp/finchat/vectorstore")
)
if os.getenv("FINCHAT_VECTORSTORE"):
    VECTORSTORE_DIR = Path(os.environ["FINCHAT_VECTORSTORE"])
elif (_repo_store / "chroma.sqlite3").exists():
    # A prebuilt index shipped with the repo (e.g. on Hugging Face Spaces) —
    # use it directly so the app never rebuilds on startup.
    VECTORSTORE_DIR = _repo_store
else:
    VECTORSTORE_DIR = _default_store

# --- SEC EDGAR corpus -------------------------------------------------------
# Recent 10-K filings for recognizable companies, fetched from SEC EDGAR via
# edgartools. The set overlaps with the FinanceBench benchmark (matching
# company + fiscal year), so FinChat can be scored against it.
# SEC requires a contact identity (name/email) on every request.
EDGAR_IDENTITY = "narendra.daffa08@gmail.com"

# (ticker, display name, fiscal year). fiscal_year matches the filing's
# period_of_report year, which correctly handles offset fiscal years
# (e.g. Amcor closes in June, Nike in May).
TARGET_FILINGS = [
    ("AMD",  "Advanced Micro Devices", 2022),
    ("AXP",  "American Express",        2022),
    ("BA",   "Boeing",                  2022),
    ("PEP",  "PepsiCo",                 2022),
    ("AMCR", "Amcor",                   2023),
    ("MMM",  "3M",                      2022),
    ("JNJ",  "Johnson & Johnson",       2022),
    ("CVS",  "CVS Health",              2022),
    ("PFE",  "Pfizer",                  2021),
    ("AES",  "AES Corporation",         2022),
    ("VZ",   "Verizon",                 2022),
    ("BBY",  "Best Buy",                2023),
    ("ADBE", "Adobe",                   2022),
    ("ULTA", "Ulta Beauty",             2023),
    ("KO",   "Coca-Cola",               2022),
    ("MSFT", "Microsoft",               2023),
    ("NKE",  "Nike",                    2023),
    ("GLW",  "Corning",                 2022),
]

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
