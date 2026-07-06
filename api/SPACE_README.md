---
title: FinChat API
emoji: 💬
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# FinChat API (headless)

FastAPI backend for **FinChat** - a Retrieval-Augmented Generation chatbot over
SEC 10-K filings. This Space is **headless**: it has no UI of its own. It serves
a JSON API that the FinChat web app (hosted on Vercel) calls.

**Endpoints**

| Method | Path         | Purpose                                  |
|--------|--------------|------------------------------------------|
| GET    | `/health`    | Liveness probe                           |
| GET    | `/companies` | Companies loaded in the corpus           |
| POST   | `/chat`      | `{question}` → `{answer, routed_to, sources}` |
| GET    | `/docs`      | Interactive Swagger UI                    |

> ⚠️ This README's front-matter (`sdk: docker`) is what tells Hugging Face to
> build the `Dockerfile` at the repo root. When you push the repo to the API
> Space, the Space's root `README.md` must contain this block.

The user-facing app lives on Vercel (set its URL after you deploy the front-end).
