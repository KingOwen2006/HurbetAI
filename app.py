"""Run with: streamlit run app.py"""

from pathlib import Path

import streamlit as st

from hurbetai.history import initialise, load_messages, save_message
from hurbetai.knowledge import answer_from_documents


PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "data"
KNOWLEDGE_ROOT = DATA_ROOT / "knowledge"
DATABASE = DATA_ROOT / "hurbetai.sqlite3"


st.set_page_config(page_title="HurbetAI", page_icon="🤖")
st.title("HurbetAI local chat")
st.caption("Questions and chat history stay on this computer. No messages are sent anywhere.")

initialise(DATABASE)

with st.sidebar:
    st.header("Local knowledge")
    st.write("Put permitted documents in `data/knowledge/`, then restart or refresh this page.")
    st.code("git clone https://github.com/twitter/the-algorithm data/knowledge/the-algorithm")
    st.warning(
        "The Algorithm is source code for a recommendation system, not a post dataset. "
        "Use it as a reference corpus unless you have a separate lawful training dataset."
    )

for role, content in load_messages(DATABASE):
    with st.chat_message(role):
        st.write(content)

if prompt := st.chat_input("Ask about your locally stored sources"):
    with st.chat_message("user"):
        st.write(prompt)
    save_message(DATABASE, "user", prompt)

    answer, sources = answer_from_documents(KNOWLEDGE_ROOT, prompt)
    with st.chat_message("assistant"):
        st.write(answer)
        if sources:
            with st.expander("Local sources used"):
                for source in sources:
                    st.code(str(source.path.relative_to(KNOWLEDGE_ROOT)))
    save_message(DATABASE, "assistant", answer)
