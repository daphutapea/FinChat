# FinChat - Complete Project Walkthrough (Study Guide)

> A top-to-bottom explanation of **every file, function, and design decision** in FinChat.
> Written so you can *understand and present* the project, not just recite it.

---

## 0. The one-sentence pitch

**FinChat is a chatbot that answers questions about 25 major companies using their official SEC 10-K annual reports - grounding every answer in the real filing (with citations), and handling both "what does the company do?" questions and "what's the revenue / quick ratio?" numeric questions.**

The core idea is **RAG (Retrieval-Augmented Generation)**: don't trust the AI to "know" facts - *retrieve* the relevant text from real documents first, then ask the AI to answer *using only that text*. That's how you make a Large Language Model (LLM) trustworthy on facts.

FinChat's twist is **hybrid RAG**: it retrieves from two kinds of data - unstructured filing *text* (for qualitative questions) **and** structured *XBRL financial data + Python-computed ratios* (for numeric questions).

---

## 1. Mental model - the two pipelines

Everything in the codebase serves one of two flows:

### A. INGESTION (run once, ahead of time) - `python -m src.ingest`
```
For each of 25 companies' 10-K filings:
   fetch filing from SEC EDGAR (edgartools)
   ├─ filing TEXT      → split into ~900-char chunks
   └─ XBRL financials  → build 5 "fact" chunks:
                            • Income Statement    (label: value)
                            • Balance Sheet       (label: value)
                            • Cash Flow Statement  (label: value)
                            • Key Ratios          (computed in Python)
                            • Financial Trends    (this year vs last year)
   → convert every chunk to an "embedding" (a vector of numbers)
   → store all vectors + metadata in a ChromaDB database ("the index")
```

### B. QUERY (every time a user asks something) - `answer(question)`
```
question
  → detect which company it's about        (routing)
  → embed the question, search the index    (semantic similarity)
  → IF it's a numeric question, ALSO force  (hybrid retrieval)
     that company's financial chunks in
  → hand the top chunks + question to the LLM
  → LLM answers using ONLY those chunks, with a "Sources:" list
```

Keep these two diagrams in your head - every function below belongs to one of them.

---

## 2. Repository map

```
FinChat/
├── app.py                     # Streamlit chat UI (the website)
├── src/
│   ├── config.py              # ALL settings in one place
│   ├── ingest.py              # BUILD-TIME: fetch → chunk → embed → store
│   ├── financials.py          # XBRL extraction + ratio/trend computation
│   └── rag.py                 # RUN-TIME: route → retrieve → generate
├── eval/
│   ├── gold_set.py            # 15 hand-written Q&A (capability test)
│   ├── run_gold.py            # capability evaluation (LLM-as-judge)
│   ├── run_eval.py            # FinanceBench benchmark evaluation
│   ├── gold_results.md        # latest capability results (93%)
│   └── results.md             # latest FinanceBench results (45%)
├── vectorstore/               # the prebuilt ChromaDB index (shipped via git-lfs)
├── requirements.txt           # pinned dependencies
├── .streamlit/config.toml     # Streamlit server settings
├── .env                       # GROQ_API_KEY (secret, gitignored)
├── README.md                  # public project page + HF Spaces config
└── DEPLOY.md                  # deployment guide
```

---

## 3. The tech stack (know every name)

| Component | Tool | Why this one |
|---|---|---|
| **LLM** (writes answers) | Llama 3.3 70B via **Groq** | Free, very fast inference |
| **Embeddings** (text → vectors) | `BAAI/bge-small-en-v1.5` | Small (~130MB), runs locally, free |
| **Vector database** | **ChromaDB** | Simple, file-based, persistent |
| **Orchestration** | **LangChain** | Standard glue for RAG components |
| **Data source** | **edgartools** | Fetches 10-Ks + XBRL from SEC EDGAR |
| **Structured data** | **XBRL** | Machine-readable financials inside every filing |
| **UI** | **Streamlit** | Chat webpage in ~85 lines |
| **Hosting** | **Hugging Face Spaces** | Free public deployment |
| **Big files** | **git-lfs** | Ships the ~160MB prebuilt index |
| **Benchmark** | **FinanceBench** | Expert-written finance-QA test set |

---

## 4. File-by-file deep dive

### 4.1 `src/config.py` - the control panel

Every tunable value lives here so you never hunt through code. Key parts:

**Vector store location logic** (lines ~21-34). This one block encodes three lessons we learned the hard way:
```python
_repo_store   = PROJECT_ROOT / "vectorstore"          # committed index
_default_store = (Path.home()/".finchat"/"vectorstore"  # Windows: home dir
                  if os.name == "nt"
                  else Path("/tmp/finchat/vectorstore"))  # Linux: /tmp
if os.getenv("FINCHAT_VECTORSTORE"):   VECTORSTORE_DIR = <env var>
elif (_repo_store/"chroma.sqlite3").exists(): VECTORSTORE_DIR = _repo_store
else: VECTORSTORE_DIR = _default_store
```
- On the **Hugging Face Space**, the prebuilt `vectorstore/chroma.sqlite3` exists in the repo → use it directly (no rebuild, instant start).
- On **Windows**, put it in the home dir - **NOT** inside OneDrive (OneDrive locks the SQLite database mid-write and corrupts it).
- On a **Linux container** without the committed index, use `/tmp` (always writable).

**`TARGET_FILINGS`** (lines ~46-73): the list of `(ticker, display name, fiscal year)` - 25 companies. The fiscal year matters because it's matched against each filing's `period_of_report` (handles companies whose fiscal year doesn't end in December, like Amcor/June, Nike/May, NVIDIA/January). These years were deliberately chosen to overlap with **FinanceBench**, so we can score against it.

**Other settings**: `CHUNK_SIZE=900`, `CHUNK_OVERLAP=150` (how filing text is split), `EMBEDDING_MODEL`, `LLM_MODEL="llama-3.3-70b-versatile"`, `LLM_TEMPERATURE=0.0` (0 = deterministic/factual, no creativity), `TOP_K=8` (how many chunks the LLM sees), `CHROMA_COLLECTION="finchat_10k"`.

---

### 4.2 `src/ingest.py` - building the index (BUILD-TIME)

**`get_filing(ticker, fiscal_year)`** - asks edgartools for a company's 10-Ks and returns the one whose `period_of_report` year matches. Robust to offset fiscal years.

**`fetch_documents()`** - the heart of ingestion. For each target company:
1. `filing.text()` → the full plain text of the 10-K.
2. Split it with **`RecursiveCharacterTextSplitter`** (chunk_size 900, overlap 150). *Why split?* Embeddings and LLMs work best on small passages; overlap avoids cutting a sentence in half across two chunks.
3. Each chunk becomes a LangChain **`Document`** = `page_content` (the text) + `metadata` (ticker, company, year, accession, source, **`type:"text"`**).
4. Then `financial_documents(...)` produces the structured chunks (`type:"financials"`).
- The `metadata` is crucial - it's what lets us later filter "only Apple" or "only financial chunks."

**`_safe_rmtree(path)`** - deletes the old index, retrying through transient file locks (another OneDrive-era defense).

**`build_vectorstore(chunks)`** - loads the embedding model and calls **`Chroma.from_documents(...)`**. This is where the magic happens: Chroma runs every chunk through the embedding model (text → a 384-number vector), and stores `(vector, text, metadata)` in a SQLite-backed database. *An embedding is a coordinate in "meaning space" - similar text lands at nearby coordinates.*

**`build_index()`** - ties it together: `fetch_documents()` → `build_vectorstore()`. It's importable so the app can bootstrap itself on first launch.

**UTF-8 fix** (lines ~31-34): `sys.stdout.reconfigure(encoding="utf-8")` - Windows terminals default to cp1252 and *crash* when `print()` hits a ™/€/curly-quote from a filing. This forces UTF-8.

---

### 4.3 `src/financials.py` - the numeric brain (the standout part)

**The problem it solves:** financial figures live in *tables*. When you convert a 10-K to plain text, tables become "number soup" - `383,285` loses its row label ("Net sales") and column ("FY2023"). Plain RAG can't answer "what's Apple's revenue?" from that. Also, LLMs are unreliable at arithmetic, so computing ratios must NOT be left to the model.

**The insight:** SEC filings ship with **XBRL** - the same numbers in machine-readable form, where every value is tagged (e.g. `us-gaap:Revenues = 383,285,000,000`). `edgartools` exposes this via `filing.obj().income_statement` / `.balance_sheet` / `.cash_flow_statement`, each convertible to a pandas DataFrame with a `standard_concept` column that *normalizes* line items across companies.

**Functions:**

- **`_value_column(df, year)`** - the statement DataFrame has one column per year (e.g. `2023-09-30`, `2022-09-24`). This finds the column for the target year.

- **`_statement_lines(stmt, year)`** - walks the rows, skips section headers/subtotals/per-segment breakdowns (`abstract`, `is_breakdown`, `dimension`), and emits clean `"label: value"` lines. Money is formatted by `_money()` ("$383.29 billion").

- **`_collect_figures(tenk, year)`** - builds a dict `{standard_concept: [(label, value)...]}` for a year. This is the raw material for computing ratios - it lets us look up "Revenue", "NetIncome", "LiabilitiesAndEquity" by their normalized tags rather than fragile label matching.

- **`_operating_cash_flow(figs)`** - special-cased because the `NetCashFromOperatingActivities` tag appears on several rows; we pick the one whose label contains "operating activ" (the true total).

- **`_compute_ratios(figs)`** - computes every ratio *in Python* (deterministic, correct). Returns `{name: (value, kind)}` where kind is `pct`/`x`/`money`. Key logic:
  - **Robust totals**: total assets via `LiabilitiesAndEquity` (accounting identity, reliable even for banks); equity via `AllEquityBalance`.
  - **Bank handling**: `is_financial = (CurrentAssetsTotal is None)` - banks have no classified balance sheet, and their revenue/COGS tags are unreliable → for them we compute *only* ROA and ROE (both from reliable NetIncome + assets/equity). This is why JPMorgan correctly shows only 2 ratios instead of nonsense margins.
  - **Sanity guard**: a margin is only kept if `abs(value) <= 1.5` (skips garbage from mis-mapped tags).
  - **Metrics**: gross/operating/net margin, capex%, asset/inventory/receivables turnover, EBITDA (= operating income + D&A), EBITDA-less-capex, ROA, ROE, current ratio, quick ratio, debt-to-equity, PP&E-as-%-of-assets, free cash flow (= operating cash flow − capex), FCF conversion.

- **`_trend_line` / `_trend_lines`** - compute the same figures/ratios for the **prior year** too, and emit "FY2023 X vs FY2022 Y (up/down Z%)" lines. Percentages change in **percentage points** (pp); dollar figures change in **%**. This is what answers "did the quick ratio improve YoY?".

- **`financial_documents(filing, ...)`** - the public entry point. Returns up to **5 Documents** per company (3 statements + Key Ratios + Financial Trends), each tagged `type:"financials"` with a keyword-rich header (so numeric queries retrieve them). The headers stuff synonyms like "revenue, margin, ratio, EBITDA..." to boost semantic matching.

---

### 4.4 `src/rag.py` - answering questions (RUN-TIME)

**`load_dotenv(PROJECT_ROOT/.env)`** - loads the `GROQ_API_KEY` by explicit path (works no matter where launched; harmless no-op on the Space where the key is a Space secret).

**`SYSTEM_PROMPT`** - the instructions given to the LLM. This is *prompt engineering* for grounding:
- "Use ONLY the provided context. Do NOT rely on outside knowledge."
- "If the answer is not in the context, reply exactly: *I couldn't find that in the filings I have.*"  ← this is why it **refuses to hallucinate**.
- "Be concise and precise with numbers. State the company and fiscal year."
- "End with a short Sources: list."

**`get_vectorstore()`** - opens the ChromaDB index (cached with `@lru_cache` so it loads once per process).

**`ensure_index()`** - if `chroma.sqlite3` doesn't exist, builds it. Subtle but important comment in the code: it checks the *filesystem*, not by opening a Chroma client - because opening a client would create an empty DB and (since chromadb caches clients per path) the later rebuild would crash. This bug cost us a deploy cycle.

**`get_llm()`** - creates the Groq LLM client; `max_retries=5` backs off through free-tier rate limits.

**Routing** - "knows where to look":
- **`company_aliases()`** builds a map from every recognizable word → ticker. It uses the ticker itself plus distinctive name-words (≥4 letters, excluding generic stopwords like "inc"/"group"). Crucially, **any alias shared by two companies is dropped** so we never mis-route.
- **`detect_ticker(question)`** - two passes: (1) an ALL-CAPS ticker in the question ("AMD"), else (2) a distinctive name word ("apple", "boeing"). Returns the ticker or `None`.

**Retrieval - the hybrid core:**
- **`_is_financial_query(question)`** - True if the question contains a money word ("revenue", "margin", "ratio", "cash flow"...).
- **`retrieve(question, ticker)`**:
  1. Semantic search the index for the top 8 chunks (filtered to the routed company if known).
  2. **Hybrid step**: if it's a financial question about a known company, do a *second* filtered search for that company's `type:"financials"` chunks (k=4), and **force them to the front** of the context. *Why:* Apple's 10-K text discusses revenue so much that the actual income-statement chunk got out-ranked; this guarantees the numbers are present.

**`format_context(docs)`** - numbers the chunks `[1] source ... [2] source ...` so the LLM can cite them.

**`answer(question)`** - the public API. `detect_ticker` → `retrieve` → build context → `PROMPT | get_llm()` (a LangChain "chain": pipe the prompt into the model) → `.invoke(...)`. Returns `{"answer", "routed_to", "sources"}`.

---

### 4.5 `app.py` - the Streamlit chat UI

- `st.set_page_config(...)` - title, icon, sidebar open by default.
- `ensure_index()` inside a spinner - on a fresh deploy, builds the index on first load.
- **Sidebar** lists `available_companies()` so users know what they can ask.
- **Starter buttons** - four example questions. Clicking one sets `st.session_state.pending` and calls `st.rerun()`; the next line reads `st.chat_input(...) or st.session_state.pop("pending", None)` so a button and the text box feed the same code path. (`st.session_state` is Streamlit's per-user memory that survives reruns.)
- **Chat loop** - stores messages in `st.session_state.messages`, renders history, and on a new question calls `answer()`, shows the answer, the "Routed to: X" badge, and an expandable **Sources** panel with the actual retrieved chunks.

---

### 4.6 Evaluation - `eval/`

Two complementary tests, both graded by an **LLM-as-judge** (a second, cheaper LLM - `llama-3.1-8b-instant` - compares FinChat's answer to a reference answer and outputs CORRECT / PARTIAL / INCORRECT). Scoring: CORRECT=1, PARTIAL=0.5, INCORRECT=0.

- **`eval/gold_set.py`** - 15 hand-written questions + reference answers (business/segments/products), verified against the filings. This is the *capability* set - the task FinChat is designed for.
- **`eval/run_gold.py`** - runs FinChat on the gold set, judges each, writes `gold_results.md`. Result: **93%**.
- **`eval/run_eval.py`** - the real **FinanceBench** benchmark:
  - `select_questions()` pulls FinanceBench 10-K questions whose `(company, fiscal year)` is in our corpus (via `FB_COMPANY_TO_TICKER`).
  - Samples an even stride of `MAX_QUESTIONS=30` to fit the free token budget.
  - Judges each vs FinanceBench's gold answer, and **breaks accuracy down by question type** (this is how we show "numeric questions went 0%→50%").
  - Result: **20% (text-only) → 45%** after adding the XBRL + ratios + trends layers.

---

### 4.7 Supporting files
- **`requirements.txt`** - dependencies **pinned to exact versions** (we learned that unpinned installs broke chromadb on the Space). Note `datasets<3.0` (older API) and `edgartools`.
- **`.streamlit/config.toml`** - `fileWatcherType="none"` (stops Streamlit's file-watcher from crawling torch and spamming errors) + headless mode.
- **README.md** - has YAML frontmatter at the top that configures the Hugging Face Space (sdk, python_version, app_file).

---

## 5. Concepts glossary (say these confidently)

- **LLM (Large Language Model)** - an AI that predicts/generates text (here: Llama 3.3 70B).
- **RAG** - retrieve relevant documents, then let the LLM answer from them. Reduces hallucination, adds citations, and lets you use private/current data the model was never trained on.
- **Embedding** - turning text into a list of numbers (a vector) so a computer can measure *meaning similarity*. Similar meanings → nearby vectors.
- **Vector store / semantic search** - a database of embeddings; given a question's embedding, it returns the closest chunks (by cosine similarity).
- **Chunk** - a small passage of a document (we use ~900 chars). We embed and retrieve chunks, not whole filings.
- **XBRL** - the structured, tagged financial data embedded in every SEC filing (revenue, assets... each machine-readable).
- **Hybrid retrieval** - combining plain semantic search with a *guaranteed* pull of structured financial chunks for numeric questions.
- **Metadata filtering** - restricting the search to chunks matching tags (e.g. `ticker=AAPL`, `type=financials`).
- **Temperature** - LLM randomness knob; 0 = deterministic/factual (what we use).
- **Prompt engineering / grounding** - writing the instructions that force the LLM to answer only from context and refuse otherwise.
- **LLM-as-judge** - using an LLM to grade another LLM's answers against a reference.
- **FinanceBench** - a hard, expert-written benchmark of finance questions over real filings.

---

## 6. Design decisions & *why* (interview gold)

1. **Why RAG, not fine-tuning?** Cheaper, no training, always cites its source, easy to update by re-ingesting.
2. **Why compute ratios in Python, not ask the LLM?** LLMs are unreliable at arithmetic; Python is exact and deterministic. This is a deliberate "don't use the hammer for a screw" choice.
3. **Why hybrid retrieval?** Financial *figures* were being out-ranked by financial *discussion* - so we guarantee the structured chunks are present for numeric questions.
4. **Why a prebuilt index shipped via git-lfs?** The free Space can't rebuild 25 filings on cold start; shipping the index makes it start instantly.
5. **Why two evaluations?** One (capability) shows what it's *for*; the other (FinanceBench) is an honest external benchmark. Reporting both - including limitations - signals engineering maturity.
6. **Why `temperature=0`?** Factual, reproducible answers.

---

## 7. Problems we hit and solved (great "tell me about a challenge" stories)

1. **"Number soup"** → XBRL structured data + deterministic ratio computation (FinanceBench 20%→45%).
2. **Retrieval ranking** → hybrid retrieval guarantees the numbers are in context.
3. **OneDrive corruption** (locked the database, then deleted the environment) → moved everything out of OneDrive.
4. **Deployment crashes** → chromadb failed on Python 3.13; fixed by pinning Python 3.12 + exact versions + shipping a prebuilt index.
5. **Bank statements break generic ratios** → detect financials (no current assets) and compute only ROA/ROE.
6. **Windows Unicode crashes, Groq token limits** → UTF-8 stdout, retry/backoff, cheap judge model.

---

## 8. The results

| Metric | Result |
|---|---|
| Corpus | 25 major companies (FY2021-2024 filings) |
| Capability eval | **93%** (15 questions) |
| FinanceBench | **20% → 45%** (numeric questions 0% → 50%); *above GPT-4's ~19% in naive RAG* |
| Deployment | Live on Hugging Face Spaces, prebuilt index via git-lfs |

---

## 9. Likely interview questions (rehearse these)

- *"What is RAG and why use it?"* → Section 5 + Design decision #1.
- *"How does it handle numbers if LLMs are bad at math?"* → Section 4.3: XBRL + Python-computed ratios (not the LLM).
- *"How do you stop it from hallucinating?"* → the SYSTEM_PROMPT grounding + "I couldn't find that" refusal.
- *"How did you evaluate it?"* → two evals, LLM-as-judge, honest 45% on FinanceBench with a numeric/qualitative breakdown.
- *"What was the hardest part?"* → number soup → hybrid XBRL retrieval; or the OneDrive/deploy saga.
- *"What would you improve next?"* → multi-step reasoning questions (agentic), a stronger embedding model, more companies.
```
