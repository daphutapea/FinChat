---
title: FinChat
emoji: 💬
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.58.0
python_version: "3.12"
app_file: app.py
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
INGESTION (once)
  fetch recent 10-Ks from SEC EDGAR ──► split into chunks
        ──► embed (local model) ──► store vectors + metadata in ChromaDB

QUERY (per question)
  question ──► detect company ──► embed ──► search (filtered by company)
        ──► top-k chunks ──► LLM ──► grounded answer + citations
```

| Layer         | Tool                                              |
|---------------|---------------------------------------------------|
| Orchestration | LangChain                                         |
| Embeddings    | `BAAI/bge-small-en-v1.5` (local, free)            |
| Vector store  | ChromaDB (persisted locally)                      |
| LLM           | Llama 3.3 70B via Groq (free)                     |
| UI            | Streamlit                                         |
| Data          | Recent SEC 10-K filings via `edgartools` (EDGAR)  |
| Evaluation    | Capability gold set + FinanceBench, LLM-as-judge  |

**Corpus — 18 recognizable companies (FY2021–2023 10-Ks):** AMD, American
Express, Boeing, PepsiCo, Amcor, 3M, Johnson & Johnson, CVS Health, Pfizer,
AES, Verizon, Best Buy, Adobe, Ulta Beauty, Coca-Cola, Microsoft, Nike, and
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

A 12-question gold set (business, segments, products) across the corpus, with
reference answers from the filings.

| CORRECT | PARTIAL | INCORRECT | Accuracy |
|---|---|---|---|
| 12 | 0 | 0 | **100%** |

**2. FinanceBench — hard external benchmark**
([`eval/results.md`](eval/results.md))

Scored on [FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench)
questions whose company + fiscal year is in the corpus.

| Accuracy | By question type |
|---|---|
| **20%** (6/30) | domain-relevant 24% · novel-generated 14% · metrics-generated 0% |

**What the gap means:** FinanceBench is dominated by *numeric financial-analysis*
questions (quick ratios, margin trends, EBITDA) that require computation over
statement tables — beyond text-retrieval RAG. FinChat's 20% is in line with the
benchmark's known difficulty (GPT-4 in a naive RAG setup scores ~19%). FinChat
is reliable at the qualitative retrieval it's designed for (100% above); closing
the numeric gap would need a financial-statement **calculation layer** — noted
as future work.

---

## ☁️ Deployment

Deployed to Hugging Face Spaces (free) — see **[DEPLOY.md](DEPLOY.md)**. The
~16k-chunk vector store is prebuilt and shipped with the repo via **git-lfs**,
so the Space starts instantly with no rebuild; `config.py` auto-detects the
committed index.

---

## ⚠️ Limitations

- **Numeric/analytical** questions (ratios, margins) require computation over
  financial-statement tables — the main gap (see Evaluation).
- The corpus is scoped to 18 companies' recent 10-Ks to stay laptop-friendly.
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
