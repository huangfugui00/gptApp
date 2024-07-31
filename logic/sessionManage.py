import streamlit as st
from typing import  List

class ChatHistory:
    user_message:str
    agent_message:str
    def __init__(self,user_message,agent_message):
        self.user_message = user_message
        self.agent_message = agent_message

class CFile:
    file_name:str=""
    pdf_show_content:str=""
    doc_list=[]
    summary:str=""
    key_point:str=""
    vector_store=None
    history:List[ChatHistory] = []

    def __init__(self,file_name,pdf_show_content,doc_list,vector_store=None):
        self.pdf_show_content = pdf_show_content
        self.file_name = file_name
        self.doc_list = doc_list
        self.history = []

    def addHistory(self,chatHistory:ChatHistory):
        self.history.append(chatHistory)

    def get_name(self):
        return self.file_name

    def is_valid(self):
        return  len(self.file_name)>0


def get_File_by_name(filename)->CFile :
    cfile = CFile("","",[],"")
    for file_obj in st.session_state['file_document']:
        if file_obj.get_name() == filename:
            return file_obj
    return cfile


def cache_add_file(cFile:CFile):
    for fileObj in st.session_state['file_document'] :
        if fileObj.get_name() == cFile.get_name():
            return
    st.session_state['file_document'].append(cFile)


def cache_clear_file(list_uploaded_file):
    filenamelist = [uploaded_file.name for uploaded_file in list_uploaded_file]
    valid_cfile = []
    for cFile in st.session_state['file_document']:
        if cFile.get_name() in filenamelist:
            valid_cfile.append(cFile)
    st.session_state['file_document'] = valid_cfile

