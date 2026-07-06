# FinChat → Vercel: turning the demo into a product

This guide moves FinChat from a single **Streamlit Space** to a proper
**two-tier product**:

- a custom **Next.js chat UI on Vercel** (your own design + domain), and
- a **headless FastAPI backend on a Hugging Face Docker Space** (your existing
  RAG code - nobody ever sees Hugging Face's UI).

Nothing about the actual RAG logic changes: the API just wraps the same
`answer()` function in [`src/rag.py`](src/rag.py) that the Streamlit app used.

```
                        ┌────────────────────────────────────────────┐
   Browser  ───────────►│  VERCEL  (this is "the product")           │
                        │   /            chat UI      (web/app/page.tsx)
                        │   /api/chat    server proxy ───────────────┐│
                        └────────────────────────────────────────────┘│
                                                                       │  (server-to-server,
                                                                       │   backend URL + secret
                                                                       ▼   stay private)
                        ┌────────────────────────────────────────────┐
                        │  HUGGING FACE DOCKER SPACE  (headless API)  │
                        │   POST /chat  ──► src.rag.answer()          │
                        │   GET  /companies, /health, /docs           │
                        └────────────────────────────────────────────┘
```

**Why this shape?** Vercel can't run Python/Streamlit or load PyTorch, so the
model has to live on a Python host. The browser never calls that host directly -
it calls a Vercel *proxy route*, which keeps the backend URL hidden and lets a
shared secret protect your Groq daily quota from abuse.

---

## What's already been built for you

| Path | What it is |
|------|-----------|
| `Dockerfile` (repo root) | Builds the API image for the HF Docker Space |
| `.dockerignore` | Keeps `venv/`, `web/`, etc. out of the image |
| `api/main.py` | FastAPI app wrapping `rag.answer()` |
| `api/requirements.txt` | Backend deps (same pinned RAG stack + FastAPI) |
| `api/SPACE_README.md` | The `sdk: docker` front-matter the Space needs |
| `web/` | The full Next.js + Tailwind chat UI for Vercel |
| `web/app/api/chat/route.ts` | Server proxy → HF Space (hides URL + adds secret) |

The backend has been smoke-tested locally: `/health`, `/companies` (returns all
25 companies), and the `/chat` input guard all pass.

---

## Prerequisites

- A **Hugging Face** account (you have one) and **git-lfs** (installed).
- A **Vercel** account - sign up free at <https://vercel.com> with your GitHub.
- A **GitHub** repo for the `web/` app (Vercel deploys from GitHub).
- (Optional, for running the UI locally) **Node.js 18+** - <https://nodejs.org>.
  You do **not** need Node to deploy; Vercel builds it in the cloud.

---

# PART A - Deploy the backend (Hugging Face Docker Space)

### A1. Confirm your Groq key

You'll paste your Groq key into the Space as a secret (never commit it). If you
want a fresh one: <https://console.groq.com> → **API Keys**.

### A2. Create a new Docker Space

1. Go to <https://huggingface.co/new-space>.
2. **Owner:** you · **Space name:** `finchat-api`.
3. **SDK:** choose **Docker** → **Blank**.
4. **Hardware:** *CPU basic* (free) · **Visibility:** *Public*.
5. **Create Space**. You now have an empty Docker Space repo.

### A3. Point the repo's README at Docker

A Docker Space builds the root `Dockerfile`, but only if the root `README.md`
front-matter says `sdk: docker`. Your current `README.md` says `sdk: streamlit`
(that was for the old Space). Replace **only the top `---` block** of
`README.md` with the one from [`api/SPACE_README.md`](api/SPACE_README.md):

```yaml
---
title: FinChat API
emoji: 💬
colorFrom: indigo
colorTo: teal
sdk: docker
app_port: 7860
pinned: false
---
```

> You're retiring the Streamlit Space, so this swap is safe. (If you ever want
> to keep both, do the API Space from a separate branch instead.)

### A4. Push the repo to the Space

From the FinChat repo root:

```bash
git lfs install

# add the new Space as a remote (replace <username>)
git remote add space-api https://huggingface.co/spaces/<username>/finchat-api

git add Dockerfile .dockerignore api/ README.md
git commit -m "Add headless FastAPI backend for Vercel front-end"

# push (LFS pushes the prebuilt vectorstore automatically)
git push space-api main
```

The `.dockerignore` keeps `venv/`, `web/`, and `node_modules/` out of the build.
The image bakes in the embedding model and the committed vector index, so the
first request is fast.

### A5. Set the Space secrets

In the Space: **Settings → Variables and secrets → New secret**

| Type   | Name              | Value |
|--------|-------------------|-------|
| secret | `GROQ_API_KEY`    | your Groq key |
| secret | `API_SECRET`      | any long random string (see below) - protects your quota |
| var    | `FRONTEND_ORIGIN` | *(optional)* your Vercel URL, e.g. `https://finchat.vercel.app` |

Generate a random `API_SECRET` (keep it - you'll reuse it on Vercel):

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

After adding secrets, **Restart** the Space so it picks them up.

### A6. Verify the backend

The Space builds in a few minutes (installing deps + baking the model). When it
says *Running*, your API is live at this **direct host** (note `.hf.space`):

```
https://<username>-finchat-api.hf.space
```

Test it (browser or curl):

- `https://<username>-finchat-api.hf.space/health` → `{"status":"healthy"}`
- `https://<username>-finchat-api.hf.space/companies` → the 25 companies
- `https://<username>-finchat-api.hf.space/docs` → interactive Swagger UI

Keep that base URL - Vercel needs it next.

---

# PART B - Deploy the front-end (Vercel)

### B1. Put `web/` on GitHub

Vercel deploys from a Git repo. Easiest: push the whole FinChat repo to GitHub
and tell Vercel the app lives in the `web/` subfolder.

```bash
git remote add origin https://github.com/<you>/finchat.git   # if not already
git push origin main
```

### B2. Import into Vercel

1. <https://vercel.com/new> → **Import** your GitHub repo.
2. **Root Directory:** click **Edit** and set it to **`web`**. *(critical - the
   Next.js app is in `web/`, not the repo root.)*
3. Framework preset auto-detects **Next.js**. Leave build settings default.

### B3. Add environment variables

In the import screen (or **Settings → Environment Variables**):

| Name          | Value |
|---------------|-------|
| `BACKEND_URL` | `https://<username>-finchat-api.hf.space` (no trailing slash) |
| `API_SECRET`  | the **same** random string you set on the Space |

### B4. Deploy

Click **Deploy**. In ~1 minute you'll get `https://<project>.vercel.app`. Open
it and ask *"What are Boeing's business segments?"* - you should get a grounded
answer with a routing badge and an expandable **sources** panel.

> **First request after idle:** the free HF Space sleeps after ~48h. The first
> question then wakes it (can take 30-60s) and may show a "waking up" message -
> just ask again once it's warm. See *Keeping it warm* below.

### B5. (Optional) Custom domain

**Vercel → Settings → Domains** → add e.g. `finchat.yourdomain.com` and follow
the DNS instructions. Now it's unmistakably a product.

---

## Running both locally (optional, needs Node)

```bash
# terminal 1 - backend
cd FinChat
venv\Scripts\activate
uvicorn api.main:app --port 7860

# terminal 2 - frontend
cd FinChat/web
npm install
copy .env.local.example .env.local     # set BACKEND_URL=http://localhost:7860
npm run dev                             # http://localhost:3000
```

---

## After it works: tidy up

1. **Update your portfolio site** - point the FinChat "Live Demo" link (in
   `Web Porto Project/index.html`) from the old HF Space to your new Vercel URL.
   Update the CV's `[Deploy]` link too.
2. **Retire the old Streamlit Space** - once the Vercel site is solid, you can
   delete `huggingface.co/spaces/<username>/Finchat` (the Streamlit one). Keep
   the new `finchat-api` Space - it's the engine.
3. **Keep the API warm (optional)** - so cold starts don't bite visitors, ping
   the Space once a day. Free option: a scheduled job at <https://cron-job.org>
   hitting `https://<username>-finchat-api.hf.space/health` every 12-24h.

---

## Cost

Everything here stays on **free tiers**: Vercel Hobby (frontend), a free HF
Docker Space (backend, ~16 GB RAM), and Groq's free LLM tier. The only limit is
Groq's ~100k tokens/day - which the `API_SECRET` protects from strangers.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Space build fails on `COPY vectorstore/` | Run `git lfs install` and confirm `vectorstore/chroma.sqlite3` is a real file (not a tiny LFS pointer) before pushing. |
| Space runs but `/companies` is empty | The index didn't ship - check the LFS push and that `FINCHAT_VECTORSTORE` points at `/home/user/app/vectorstore` (set in the Dockerfile). |
| Vercel app: "Server is missing BACKEND_URL" | Set `BACKEND_URL` in Vercel env vars and **redeploy** (env changes need a new deploy). |
| Every answer says "waking up / unreachable" | The Space is asleep or `BACKEND_URL` is wrong. Open the `/health` URL directly to wake/verify it. |
| `401 Invalid or missing API key` | `API_SECRET` differs between the Space and Vercel. Make them identical, redeploy. |
| Answers work but are slow the first time | Cold start (model + container boot). Add the keep-warm ping above. |
