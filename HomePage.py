import streamlit as st
import random
from streamlit_pdf_viewer import pdf_viewer
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ReduceDocumentsChain,StuffDocumentsChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv, find_dotenv
from logic import readPdfToDocumentList,cache_add_file,get_File_by_name,CFile,cache_clear_file
from css import css
import copy
from typing import  List
load_dotenv(find_dotenv('.env'))
api_key = os.environ.get('openai_api_key')

model_name = 'gpt-3.5-turbo-ca'

llm = ChatOpenAI(temperature=0, model_name=model_name,
                 openai_api_base="https://api.chatanywhere.tech/v1",
                 openai_api_key=api_key
                 )

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
            select_paper = st.selectbox('选择文章',
                                         [""]+[file.name for file in uploaded_files])
            cache_clear_file(uploaded_files)
            for file in uploaded_files:
                if get_File_by_name(file.name) is None:
                    doc_list = readPdfToDocumentList(copy.deepcopy(file))
                    cFile = CFile(file.name,file.read(),doc_list)
                    cache_add_file(cFile)

            if select_paper:
                upload_file = select_paper

        if is_clear_docs and 'key' in st.session_state.keys():
            clear_docs()

        return upload_file


def content_container(pdf_file_name):
    if pdf_file_name:
        file = get_File_by_name(pdf_file_name)
        import base64
        base64_pdf = base64.b64encode(file.pdf_show_content).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="98%" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)


def chat_container(pdf_file_name):
    if pdf_file_name:
        mission = st.selectbox(label="" ,options=['','总结文章','列出关键点'])
        file = get_File_by_name(pdf_file_name)
        docs = file.doc_list

        if mission == '总结文章':
            # Text summarization
            prompt = PromptTemplate(input_variables=['docs'],
                                    template=""""The following is a set of documents
                 {docs}
                 根据这个文档列表，写一个200字以内的摘要.
                 Helpful Answer:""")
            # Text summarization
            chain = LLMChain(llm=llm, prompt=prompt)#比chain = load_summarize_chain(llm, chain_type='map_reduce')更快，消耗的token也基本一样，且只需要调用一次#与chain = load_summarize_chain(llm, chain_type='stuff')一致；自己创建prompt的好处就是可以自定义，推荐
            content = chain.invoke(docs)
            st.write(content['text'])
            pass
        elif mission == "列出关键点":
            prompt = PromptTemplate(input_variables=['docs'],
                                               template=""""The following is a set of documents
                {docs}
                根据这个文档列表，列出十个最重要的关键词
                Helpful Answer:""")
            # Text summarization
            chain = LLMChain(llm=llm, prompt=prompt)
            content = chain.invoke({"docs":docs})
            st.write(content['text'])


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


