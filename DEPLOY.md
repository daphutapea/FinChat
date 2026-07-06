# Deploying FinChat to Hugging Face Spaces

A free, step-by-step guide to putting FinChat online with a public link.

---

## 0. Before you start

1. **Rotate your Groq API key.** Go to <https://console.groq.com> → *API Keys* → create a new
   key. You'll paste the new key into the Space as a secret (never commit it).
2. Create a free **Hugging Face account**: <https://huggingface.co/join>.
3. Make sure **git** is installed (it is on this machine).

---

## 1. Create the Space

1. Go to <https://huggingface.co/new-space>.
2. **Owner:** you. **Space name:** `finchat`.
3. **SDK:** choose **Streamlit**.
4. **Hardware:** *CPU basic* (free). **Visibility:** *Public*.
5. Click **Create Space**. You now have an empty Space repo.

---

## 2. Add your API key as a secret

In your Space: **Settings → Variables and secrets → New secret**
- **Name:** `GROQ_API_KEY`
- **Value:** your Groq key

The app reads this automatically (`os.getenv("GROQ_API_KEY")`), so no `.env` is
needed on the Space.

---

## 3. Push the code

From the project root:

```bash
git init
git add .
git commit -m "FinChat: RAG chatbot over SEC 10-K filings"

# Connect to your Space (replace <username>)
git remote add space https://huggingface.co/spaces/<username>/finchat
git push space main
```

> `.gitignore` already excludes `.env`, `venv/`, `data/`, and `vectorstore/`,
> so your key and large files stay out of the repo.

The Space will build (install `requirements.txt`) and start. **On first load,
the app builds the vector store itself** (downloads the dataset + embeds the
chunks). On free CPU this takes roughly **5-8 minutes** the first time - the UI
shows *"Preparing the knowledge base..."*. After that it's fast.

---

## 4. (Optional) Instant cold starts - commit the prebuilt index

Free Spaces sleep after inactivity and rebuild the index on wake (~5-8 min),
which is slow for someone clicking your link cold. To make cold starts
**instant**, commit the prebuilt vector store using **git-lfs** (it's ~66 MB).

```bash
# One-time: install git-lfs from https://git-lfs.com then:
git lfs install

# Copy the prebuilt store into the repo
mkdir vectorstore
cp -r ~/.finchat/vectorstore/* vectorstore/     # Windows: xcopy /E /I %USERPROFILE%\.finchat\vectorstore vectorstore

# Track the large binary files with LFS
git lfs track "vectorstore/**"
git add .gitattributes

# Stop ignoring the committed store, then commit it
#   -> remove the "vectorstore/" line from .gitignore first
git add vectorstore .gitignore
git commit -m "Add prebuilt vector store for instant startup"
git push space main
```

Then, in the Space **Settings → Variables and secrets**, add a **variable**
(not a secret):
- **Name:** `FINCHAT_VECTORSTORE`
- **Value:** `vectorstore`

Now `ensure_index()` finds the committed store and skips the rebuild entirely.

---

## 5. Verify

1. Open your Space URL.
2. Wait for the first load (see the spinner if it's building).
3. Ask: *"What are AMD's main business risks?"* - you should get a grounded
   answer with a *Sources* panel and a routing badge.
4. Add the live link to the top of `README.md` and to your portfolio.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `GROQ_API_KEY is not set` | Add the secret (Step 2) and *Restart* the Space. |
| Build error on `datasets` | Confirm `requirements.txt` pins `datasets<3.0`. |
| Stuck on "Preparing the knowledge base" | First build is slow on free CPU; wait, or use Step 4. |
| Sidebar hidden | Click the **›** at the top-left to expand it. |
