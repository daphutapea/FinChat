"""FinChat - Streamlit chat UI.

Run from the project root:
    streamlit run app.py
"""
import streamlit as st

from src.rag import answer, available_companies, ensure_index

st.set_page_config(
    page_title="FinChat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("💬 FinChat")
st.caption(
    "Ask questions about companies' SEC 10-K filings. "
    "Every answer is grounded in the filings, with sources you can inspect."
)

# On a fresh deployment (e.g. Hugging Face Spaces) the vector store won't exist
# yet -- build it once on first load. On later runs this is a fast no-op.
with st.spinner("Preparing the knowledge base (first run only, please wait)…"):
    ensure_index()

# --- sidebar: which companies are available ---------------------------------
with st.sidebar:
    st.header("📚 Companies loaded")
    for ticker, name in available_companies():
        st.markdown(f"- **{ticker}** — {name}")
    st.caption("Source: SEC 10-K filings, 2017–2020.")

# --- starter questions (clickable examples) ---------------------------------
STARTER_QUESTIONS = [
    "What are AMD's main business risks?",
    "What are Abbott's business segments?",
    "What is Air Products' primary business?",
    "What does Matson's logistics business do?",
]

# --- chat history -----------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Clickable examples, shown only until the first question is asked.
if not st.session_state.messages and "pending" not in st.session_state:
    st.markdown("**Try one of these to get started:**")
    cols = st.columns(2)
    for i, example in enumerate(STARTER_QUESTIONS):
        if cols[i % 2].button(example, use_container_width=True):
            st.session_state.pending = example
            st.rerun()

# --- new question -----------------------------------------------------------
# A question can arrive from the chat box or from a starter button.
prompt = st.chat_input("e.g. What were AMD's main risk factors?") or st.session_state.pop("pending", None)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the filings..."):
            result = answer(prompt)

        st.markdown(result["answer"])

        if result["routed_to"]:
            st.caption(f"🔎 Routed retrieval to: **{result['routed_to']}**")

        with st.expander(f"📄 Sources ({len(result['sources'])})"):
            for i, doc in enumerate(result["sources"], 1):
                st.markdown(f"**[{i}] {doc.metadata.get('source', '')}**")
                st.write(doc.page_content[:500] + "…")

    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"]}
    )
