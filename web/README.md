# FinChat - Web front-end (Next.js)

A polished chat UI for **FinChat**, deployed on **Vercel**. It has no model code
of its own: it calls the FinChat API (a headless Hugging Face Docker Space) over
HTTP, through a server-side proxy that keeps the backend URL and secret private.

```
Browser ──► Vercel (this app)
               ├─ /            chat UI (app/page.tsx)
               └─ /api/chat    server proxy ──► HF Docker Space  /chat ──► rag.answer()
```

## Local development

```bash
cd web
npm install
cp .env.local.example .env.local     # then edit BACKEND_URL
npm run dev                          # http://localhost:3000
```

You need the FinChat API running somewhere and its URL in `BACKEND_URL`
(either your deployed HF Space, or a local `uvicorn api.main:app --port 7860`
with `BACKEND_URL=http://localhost:7860`).

## Environment variables

| Name          | Required | Description                                              |
|---------------|----------|----------------------------------------------------------|
| `BACKEND_URL` | yes      | Base URL of the FinChat API (HF Space), no trailing slash |
| `API_SECRET`  | no       | If set on the Space, the same value here authenticates the proxy |

Set both in **Vercel → Project → Settings → Environment Variables**, then redeploy.

See [`../MIGRATE_TO_VERCEL.md`](../MIGRATE_TO_VERCEL.md) for the full deploy guide.
