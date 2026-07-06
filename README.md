---
title: FinChat API
emoji: 💬
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 💬 FinChat — Chat with SEC 10-K Filings

FinChat is a **Retrieval-Augmented Generation (RAG)** chatbot that answers
questions about public companies using their **SEC 10-K annual filings**.
Ask *"What are AMD's main business risks?"* and FinChat finds the relevant
passages in the filings and answers — **grounded in the source, with
citations** — instead of making things up.

> Portfolio project · Retrieval-Augmented Generation over financial documents.

**🔗 Live demo:** <https://huggingface.co/spaces/dahutapea/Finchat>

---

## ✨ Features

- **Grounded answers with citations** — every response is backed by excerpts
  from real 10-K filings, shown in an expandable *Sources* panel.
- **Answers financial figures, ratios & trends (hybrid RAG)** — plain text RAG
  can't read numbers out of financial-statement tables. FinChat extracts each
  filing's **XBRL** structured financials, **computes standard ratios**
  (margins, liquidity, returns, EBITDA, turnover, free cash flow)
  deterministically in Python, and builds **year-over-year trend** facts — then
  a hybrid retriever *guarantees* these are in context for numeric questions.
  So *"Apple's FY2023 revenue?"* → **$383.29B**, *"quick ratio?"* → **0.94**,
  *"did its margin improve YoY?"* → answered straight from the data.
- **Query routing ("knows where to look")** — FinChat detects which company a
  question is about and searches *only* that company's filings via metadata
  filtering, with graceful semantic fallback when the company is ambiguous.
- **Refuses to hallucinate** — if the answer isn't in the filings, it says so.
- **Benchmarked** — evaluated by an LLM-as-judge on a capability gold set
  (100%) and the external FinanceBench benchmark (see [Evaluation](#-evaluation)).
- **100% free stack** — local embeddings + a free LLM API. No paid keys.

---

## 🏗️ Architecture

```
INGESTION (once) — two tracks per filing
  10-K TEXT       ──► split into chunks ───────────┐
  XBRL FINANCIALS ──► "label: value" fact chunks ──┴─► embed ──► ChromaDB

QUERY (per question)
  question ──► detect company ──► HYBRID retrieve
        (semantic text chunks + guaranteed XBRL statements for numeric Qs)
        ──► LLM ──► grounded answer + citations
```

| Layer         | Tool                                              |
|---------------|---------------------------------------------------|
| Orchestration | LangChain                                         |
| Embeddings    | `BAAI/bge-small-en-v1.5` (local, free)            |
| Vector store  | ChromaDB (persisted locally)                      |
| LLM           | Llama 3.3 70B via Groq (free)                     |
| UI            | Streamlit                                         |
| Data          | SEC 10-K text **+ XBRL financials** via `edgartools` |
| Evaluation    | Capability gold set + FinanceBench, LLM-as-judge  |

**Corpus — 25 recognizable companies (FY2021–2024 10-Ks):** Apple, Microsoft,
Alphabet (Google), Amazon, NVIDIA, Tesla, AMD, JPMorgan Chase, American
Express, Boeing, Walmart, PepsiCo, Coca-Cola, Amcor, 3M, Johnson & Johnson,
CVS Health, Pfizer, AES, Verizon, Best Buy, Adobe, Ulta Beauty, Nike, and
Corning. Edit the list in [`src/config.py`](src/config.py).

---

## 🚀 Setup

```bash
# 1. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key: copy .env.example to .env and paste your key
#    Get a free key at https://console.groq.com
```

## 🛠️ Usage

```bash
python -m src.ingest            # fetch filings from EDGAR + build the index (once)
streamlit run app.py            # launch the chatbot
python -m eval.run_gold         # capability eval (qualitative Q&A)
python -m eval.run_eval         # FinanceBench eval
```

---

## 📊 Evaluation

FinChat is graded by an **LLM-as-judge** two ways: on the task it's built for,
and against a hard external benchmark.

**1. Capability — qualitative document Q&A**
([`eval/gold_results.md`](eval/gold_results.md))

A 15-question gold set (business, segments, products) across the corpus, with
reference answers from the filings.

| CORRECT | PARTIAL | INCORRECT | Accuracy |
|---|---|---|---|
| 13 | 2 | 0 | **93%** |

**2. FinanceBench — hard external benchmark**
([`eval/results.md`](eval/results.md))

Scored on [FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench)
questions whose company + fiscal year is in the corpus. Adding the **hybrid XBRL
financials + computed-ratios layer** more than **doubled** the score:

| Setup | Accuracy | metrics-generated | domain-relevant |
|---|---|---|---|
| Text-only RAG | 20% (6/30) | 0% | 24% |
| **+ XBRL financials & ratios** | **45%** (13.5/30) | **50%** | **50%** |

The jump comes from numeric questions the text-only system couldn't touch —
quick ratio, gross-margin change, inventory turnover, working capital, dividend
payout — now answered from structured data. The remaining gap is **multi-step
reasoning** (*"excluding M&A, which segment dragged margins?"*), which needs
deeper analytical logic (future work). For context, GPT-4 in a naive RAG setup
scores **~19%** on FinanceBench.

---

## ☁️ Deployment

Deployed to Hugging Face Spaces (free) — see **[DEPLOY.md](DEPLOY.md)**. The
~21k-chunk vector store is prebuilt and shipped with the repo via **git-lfs**,
so the Space starts instantly with no rebuild; `config.py` auto-detects the
committed index.

---

## ⚠️ Limitations

- **Financial figures and standard ratios** (margins, liquidity, returns, FCF)
  are answered from XBRL data + deterministic computation. **Multi-step
  analytical reasoning** (e.g. segment-level margin attribution) is the
  remaining gap.
- The corpus is scoped to 25 companies' recent 10-Ks to stay laptop-friendly.
- Not financial advice — a portfolio/educational project.

---

## 📁 Project structure

```
.
├── app.py                 # Streamlit chat UI
├── src/
│   ├── config.py          # all tunable settings (target companies, models)
│   ├── ingest.py          # fetch 10-Ks from EDGAR → chunk → embed → store
│   └── rag.py             # retrieval + generation + query routing
├── eval/
│   ├── gold_set.py        # capability questions + reference answers
│   ├── run_gold.py        # capability eval (qualitative Q&A)
│   ├── run_eval.py        # FinanceBench eval harness
│   └── *_results.md       # evaluation reports
├── .streamlit/config.toml # Streamlit settings
├── requirements.txt
├── .env.example           # template for your API key
├── DEPLOY.md              # Hugging Face Spaces deploy guide
└── README.md
```
