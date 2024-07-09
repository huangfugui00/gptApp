import streamlit as st
from typing import  List


class CFile:
    def __init__(self,file_name,pdf_show_content,doc_list):
        self.pdf_show_content = pdf_show_content
        self.file_name = file_name
        self.doc_list = doc_list

    def get_name(self):
        return self.file_name


def get_File_by_name(filename):
    for file_obj in st.session_state['file_document']:
        if file_obj.get_name() == filename:
            return file_obj
    return None


def cache_add_file(cFile:CFile):
    for fileObj in st.session_state['file_document'] :
        if fileObj.get_name() == cFile.get_name():
            return
    st.session_state['file_document'].append(cFile)


def cache_clear_file(list_uploaded_file):
    filenamelist=[uploaded_file.name for uploaded_file in list_uploaded_file]
    valid_cfile = []
    for cFile in st.session_state['file_document']:
        if cFile.get_name() in filenamelist:
            valid_cfile.append(cFile)
    st.session_state['file_document'] = valid_cfile

