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
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))
api_key = os.environ.get('openai_api_key')


from logic import get_upload_file,cache_file

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",
                 openai_api_base="https://api.chatanywhere.tech/v1",
                 openai_api_key=api_key
                 )


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


def chat_container(pdf_file):
    st.write("chat")
    if pdf_file:
        mission = st.selectbox(label="" ,options=['','总结文章','列出关键点'])
        if mission == '总结文章':
            pdf_reader = PdfReader(pdf_file)

            texts = [page.extract_text() for page in pdf_reader.pages]
            # texts = text_splitter.split_text(str(pdf_file.read(),encoding='utf-8'))
            # Create multiple documents
            docs = [Document(page_content=t) for t in texts]

            # Text summarization
            prompt = PromptTemplate(input_variables=['docs'],
                                    template=""""The following is a set of documents
                 {docs}
                 根据这个文档列表，写一个500字以内的摘要.
                 Helpful Answer:""")
            # Text summarization
            chain = LLMChain(llm=llm, prompt=prompt)
           # chain = load_summarize_chain(llm, chain_type='map_reduce')
            content = chain.invoke(docs)
            st.write(content['text'])
            pass
        elif mission == "列出关键点":
            pdf_reader = PdfReader(pdf_file)

            texts = [page.extract_text() for page in pdf_reader.pages]


            # texts = text_splitter.split_text(str(pdf_file.read(),encoding='utf-8'))
            # Create multiple documents
            docs = [Document(page_content=t) for t in texts]

            prompt = PromptTemplate(input_variables=['docs'],
                                               template=""""The following is a set of documents
                {docs}
                根据这个文档列表，列出十个最重要的关键词
                Helpful Answer:""")
            # Text summarization
            chain = LLMChain(llm=llm, prompt=prompt)
            content = chain.invoke(docs)
            st.write(content['text'])
        elif mission == "列出关键点1":
            pdf_reader = PdfReader(pdf_file)
            texts = [page.extract_text() for page in pdf_reader.pages]
            # texts = text_splitter.split_text(str(pdf_file.read(),encoding='utf-8'))
            # Create multiple documents
            docs = [Document(page_content=t) for t in texts]

            text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=2000, chunk_overlap=50)
            docs = text_splitter.split_documents(docs)
            # texts = text_splitter.split_text(str(pdf_file.read(),encoding='utf-8'))
            # Create multiple documents
            # docs = [Document(page_content=t) for t in texts]
            map_template_name = PromptTemplate(input_variables=['docs'],
                                               template=""""The following is a set of documents
            {docs}
            Based on this list of docs, give me main key points
            Helpful Answer:""")
            map_chain = LLMChain(llm=llm, prompt=map_template_name)
            combine_documents_chain = StuffDocumentsChain(
                llm_chain=map_chain, document_variable_name="docs"
            )
            reduce_documents_chain = ReduceDocumentsChain(
                # This is final chain
                combine_documents_chain=combine_documents_chain,
                # If documents exceed context for `StuffDocumentsChain`
                collapse_documents_chain=combine_documents_chain,
                # The maximum number of tokens to group documents into.
                token_max=500,
            )
            output = reduce_documents_chain.run(docs)
            st.write(output)
    pass


def main():
    page_layout_view()
    upload_file = sidebar_view()
    col1, col2 = st.columns(2)
    with col1:
        content_container(upload_file)
    with col2:
        chat_container(upload_file)


main()


