# Archive

Retired files from FinChat's original **Streamlit** version, kept here for
reference after the migration to a **Next.js front-end (Vercel) + FastAPI
backend (Hugging Face Docker Space)**. Nothing in this folder is used by the
current app or by either deployment - it's safe to delete if you ever want to.

| File | What it was |
|------|-------------|
| `app.py` | The Streamlit chat UI - entry point for `streamlit run app.py`. Replaced by `web/` (Vercel UI) + `api/main.py` (FastAPI). |
| `streamlit_app.py` | A leftover Streamlit starter template (the spiral demo); never used. |
| `streamlit-config.toml` | The old `.streamlit/config.toml` theme/config. |
| `DEPLOY.md` | The old guide for deploying to a Streamlit Hugging Face Space. Superseded by `../MIGRATE_TO_VERCEL.md`. |
