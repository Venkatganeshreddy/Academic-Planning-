"""NIAT Learning Copilot — dashboard router.

Three pages: Chat (ask the data), Knowledge Base (per-university catalog), and
Pipeline (how the data is built). Shared infra lives in aip/dashboard.py.

Run locally:  streamlit run app.py
Deploy:       Streamlit Cloud, with secrets OPENROUTER_API_KEY / AIP_MODEL.
"""
import streamlit as st

from aip import dashboard
from views import chat, knowledge_base, pipeline

st.set_page_config(page_title="NIAT Learning Copilot", page_icon="🎓", layout="wide")

dashboard.db_path()      # build the DB once per boot (cached)
dashboard.inject_css()

pg = st.navigation([
    st.Page(chat.render, title="Chat", icon="💬", default=True),
    st.Page(knowledge_base.render, title="Knowledge Base", icon="📚"),
    st.Page(pipeline.render, title="Pipeline", icon="🔧"),
])
pg.run()
