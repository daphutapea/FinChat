# FinChat API — headless FastAPI service for a Hugging Face Docker Space.
#
# IMPORTANT: build context is the repo ROOT, so the image can COPY the RAG code
# in src/ and the prebuilt vector index in vectorstore/ (shipped via git-lfs).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 1) Install Python deps as root -> system site-packages (readable by all users).
COPY api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# 2) Non-root user (Hugging Face Spaces convention: uid 1000).
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/.cache/huggingface
WORKDIR /home/user/app

# 3) Pre-download the embedding model INTO the image (as the runtime user), so
#    the first request is fast and needs no network at runtime.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# 4) App code + the prebuilt vector index.
COPY --chown=user src/ ./src/
COPY --chown=user vectorstore/ ./vectorstore/
COPY --chown=user api/ ./api/

# Point config at the committed, writable index (chromadb opens it read/write).
ENV FINCHAT_VECTORSTORE=/home/user/app/vectorstore

EXPOSE 7860
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
