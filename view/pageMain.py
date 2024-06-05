import streamlit as st
from .sidebarView import sidebar_view
from .col1View import col1_view
from .col2View import col2_view


def page_layout_view():
    st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
    st.header("📖KnowledgeGPT")


def page_main():
    page_layout_view()
    sidebar_view()
    col1, col2 = st.columns(2)
    with col1:
        col1_view()
    with col2:
        col2_view()




