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

<!-- After deploying, add your live link here:
**🔗 Live demo:** https://huggingface.co/spaces/<your-username>/finchat -->

---

## ✨ Features

- **Grounded answers with citations** — every response is backed by excerpts
  from real 10-K filings, shown in an expandable *Sources* panel.
- **Query routing ("knows where to look")** — FinChat detects which company a
  question is about and searches *only* that company's filings via metadata
  filtering, with graceful semantic fallback when the company is ambiguous.
- **Refuses to hallucinate** — if the answer isn't in the filings, it says so.
- **Benchmarked** — an LLM-as-judge evaluation scores answers against a
  curated gold set (see [Evaluation](#-evaluation)).
- **100% free stack** — local embeddings + a free LLM API. No paid keys.

---

## 🏗️ Architecture

```
INGESTION (once)
  10-K sentences ──► reassemble into sections ──► split into chunks
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
| Data          | `JanosAudran/financial-reports-sec` (10-K text)   |
| Evaluation    | Curated gold set + LLM-as-judge                   |

**Companies in the demo corpus (2017–2020 filings):** AMD, Abbott (ABT),
Air Products (APD), AAR Corp (AIR), Matson (MATX). Swap them in
[`src/config.py`](src/config.py).

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
python -m src.ingest --list     # see which companies are available
python -m src.ingest            # build the vector store (run once)
streamlit run app.py            # launch the chatbot
python -m eval.run_eval         # run the evaluation
```

---

## 📊 Evaluation

FinChat is graded by an **LLM-as-judge** against a **12-question curated gold
set** whose reference answers are written from the 2017–2020 filings in the
corpus (see [`eval/gold_set.py`](eval/gold_set.py)). Full report:
[`eval/results.md`](eval/results.md).

| Metric | top-5 (baseline) | **top-8 (tuned)** |
|---|---|---|
| CORRECT / PARTIAL / INCORRECT | 7 / 4 / 1 | **10 / 2 / 0** |
| **Accuracy** (CORRECT=1, PARTIAL=0.5) | 75% | **92%** |

Increasing retrieval depth from **top-5 to top-8 chunks** lifted accuracy from
**75% → 92%** and eliminated the incorrect answer, with **no regressions** — the
earlier misses were passages that existed in the filings but fell just outside
the top-5.

**Error analysis (remaining misses)**
- ✅ Structural questions (segments, services, products, primary business) are
  answered correctly across all companies.
- ⚠️ The 2 remaining PARTIALs are exhaustive-list / framing recall gaps: the
  risk-factor answer omits "competition," and the Matson answer omits the
  "China" expedited service — the relevant passage is worded differently from
  the question.

*A corpus-aligned gold set was used because the dataset ends in 2020 while the
FinanceBench benchmark targets 2018–2023 filings, so direct benchmark overlap
is thin.*

---

## ☁️ Deployment

Deploy to Hugging Face Spaces (free) — see **[DEPLOY.md](DEPLOY.md)** for
step-by-step instructions. The app **self-builds** the vector store on first
load, so no prebuilt index is required.

---

## ⚠️ Limitations

- Answers are only as good as the retrieved passages; **numeric/table**
  questions are the hardest part of financial RAG.
- The corpus is scoped to 5 companies / recent years to stay laptop-friendly.
- Not financial advice — a portfolio/educational project.

---

## 📁 Project structure

```
.
├── app.py                 # Streamlit chat UI
├── src/
│   ├── config.py          # all tunable settings
│   ├── ingest.py          # build the vector store (load→section→chunk→embed→store)
│   └── rag.py             # retrieval + generation + query routing
├── eval/
│   ├── gold_set.py        # curated questions + reference answers
│   ├── run_eval.py        # LLM-as-judge evaluation harness
│   └── results.md         # latest evaluation report
├── .streamlit/config.toml # Streamlit settings
├── requirements.txt
├── .env.example           # template for your API key
├── DEPLOY.md              # Hugging Face Spaces deploy guide
└── README.md
```
