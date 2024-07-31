import streamlit as st
import random
from streamApp.logic.LLMLogic import qa_web,qa_sources,doc_to_vecstore,qa_sources_db
from streamApp.logic.sessionManage import cache_add_file,cache_clear_file,get_File_by_name,CFile,ChatHistory
from streamApp.logic.fileLogic import readPdfToDocumentList
from css import css
import copy
from typing import List
import streamlit_antd_components as sac


if 'file_document' not in st.session_state.keys():
    st.session_state['file_document']: List[CFile] = []


def page_layout_view():
    st.set_page_config(page_title="KnowledgeGPT", page_icon="📖", layout="wide")
    st.header("📖知识GPT")
    st.write(css, unsafe_allow_html=True)


def clear_docs():
    st.session_state.pop('key')
    st.session_state.pop('file_document')
    st.rerun()


def sidebar_view():
    with st.sidebar:
        st.success("在上方选择一个页面。")
        st.write("文件上传")
        if 'key' not in st.session_state: st.session_state.key = str(random.randint(1000, 100000000))
        uploaded_files = st.file_uploader(
            "Upload a pdf, docx, or txt file",
            type=["pdf", "docx", "txt"],
            help="Scanned documents are not supported yet!",
            accept_multiple_files=True,
            label_visibility="collapsed",
            key = st.session_state.key
        )

        is_clear_docs = st.button("清空文档", type="primary")
        upload_file = None
        if uploaded_files:

            cache_clear_file(uploaded_files)
            for file in uploaded_files:
                cFile = get_File_by_name(file.name)
                if not cFile.is_valid():
                    doc_list = readPdfToDocumentList(copy.deepcopy(file))
                    db = doc_to_vecstore(file.name,doc_list)
                    cFile = CFile(file.name,file.read(),doc_list,db)
                    cache_add_file(cFile)
            select_paper = st.selectbox('选择文章',
                                        [""] + [file.name for file in uploaded_files])
            if select_paper:
                upload_file = select_paper

        if is_clear_docs and 'key' in st.session_state.keys():
            clear_docs()

        return upload_file


def content_container(pdf_file_name):
    if pdf_file_name:
        file = get_File_by_name(pdf_file_name)
        if file.is_valid():
            import base64
            base64_pdf = base64.b64encode(file.pdf_show_content).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="98%" height="1000" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

def _show_chat_history(cfile:CFile):
    num_history = len(cfile.history)
    messages = st.container(height=760)
    for i in range(num_history):
        chat_history = cfile.history[num_history-1-i]
        messages.chat_message("assistant").write(f"Echo: {chat_history.agent_message}")
        messages.chat_message("user").write(chat_history.user_message)

def chat_container(pdf_file_name):
    if pdf_file_name:
        mission = st.selectbox(label="预定功能选项" ,options=['','总结文章','列出关键点'])
        file = get_File_by_name(pdf_file_name)
        if not  file.is_valid():
            return
        docs = file.doc_list
        vector_store = file.vector_store
        if mission == '总结文章':
            # Text summarization
            if file.summary :
                content = file.summary
            else:
                content = qa_sources(docs, '写一个500字以内的摘要')
                file.summary = content
            st.write(content)

        elif mission == "列出关键点":
            if file.key_point:
                content = file.key_point
            else:
                content = qa_sources(docs, '列出十个最重要的关键词')
                file.key_point = content
            st.write(content)

        st.write("\n")

        question = st.chat_input("边看文档，边提问", max_chars=100)


        if question :
            content = qa_sources(vector_store, question)
            chatHistory = ChatHistory(question,content)
            file.addHistory(chatHistory)
        _show_chat_history(file)



def main():
    page_layout_view()
    upload_file = sidebar_view()
    if upload_file is None: #多pdf问答
        pass
    else: #单个pdf问答
        col1, col2 = st.columns(2)
        with col1:
            content_container(upload_file)
        with col2:
            chat_container(upload_file)


main()


