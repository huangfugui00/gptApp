import streamlit as st
import random
from streamlit_pdf_viewer import pdf_viewer
from logic import get_upload_file,cache_file


def page_layout_view():
    st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
    st.header("📖知识GPT")


def clear_docs():
    st.session_state.pop('key')
    st.session_state.pop('uploaded_files')
    st.rerun()


def sidebar_view():
    st.sidebar.success("在上方选择一个页面。")
    st.sidebar.write("文件上传")
    if 'key' not in st.session_state: st.session_state.key = str(random.randint(1000, 100000000))
    uploaded_files = st.sidebar.file_uploader(
        "Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt"],
        help="Scanned documents are not supported yet!",
        accept_multiple_files=True,
        label_visibility="collapsed",
        key = st.session_state.key
    )

    is_clear_docs = st.sidebar.button("清空文档", type="primary")
    upload_file = None
    if uploaded_files:
        select_paper = st.sidebar.selectbox('选择文章',
                                     [""]+[file.name for file in uploaded_files])
        cache_file(uploaded_files)
        if select_paper:
            upload_file = get_upload_file(select_paper)

    if is_clear_docs and 'key' in st.session_state.keys():
        clear_docs()

    return upload_file


def content_container(pdf_file):
    st.write("文本内容")
    if pdf_file:
        binary_data = pdf_file.getvalue()
        pdf_viewer(input=binary_data,
                  height=700)

def chat_container():
    st.write("chat")
    pass


def main():
    page_layout_view()
    upload_file = sidebar_view()
    col1, col2 = st.columns(2)
    with col1:
        content_container(upload_file)
    with col2:
        chat_container()


main()


