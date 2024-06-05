import streamlit as st
import random


def process_file(uploaded_files):
    st.session_state['uploaded_files']=uploaded_files


def clear_docs():
    st.session_state.pop('key')
    st.session_state.pop('uploaded_files')
    st.rerun()


def sidebar_view():
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
    if uploaded_files:
        user_food = st.sidebar.selectbox('选择文章',
                                     [""]+[file.name for file in uploaded_files])
        process_file(uploaded_files)


    if is_clear_docs and 'key' in st.session_state.keys():
        clear_docs()


