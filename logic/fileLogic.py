import streamlit as st
from PyPDF2 import PdfReader
from langchain.docstore.document import Document

def file_type(filename):
    return filename.split(".")[-1]


def cache_file(uploaded_files):
    st.session_state['uploaded_files']=uploaded_files



def get_upload_file(filename):
    if 'uploaded_files' in st.session_state.keys():
        for file in st.session_state["uploaded_files"]:
            if file.name == filename:
                if file_type(filename) == "pdf":
                    return file


def readPdfToDocumentList(file):
    pdf_reader = PdfReader(file)
    texts = [page.extract_text() for page in pdf_reader.pages]
    docs = [Document(page_content=t) for t in texts]
    return docs