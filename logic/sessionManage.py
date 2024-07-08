import streamlit as st
from typing import  List


class File:
    def __init__(self,file,doc_list):
        self.file = file
        self.doc_list = doc_list

    def get_name(self):
        return self.file.name


def get_File_by_name(filename):
    for file_obj in st.session_state['file_document']:
        if file_obj.file.name == filename:
            return file_obj


def cache_add_file(file,document_list):
    if 'file_document' not in st.session_state.keys():
        st.session_state['file_document'] : List[File]= []

    for fileObj in st.session_state['file_document'] :
        if fileObj.get_name() == file.name:
            return
    fileObj = File(file,doc_list=document_list)
    st.session_state['file_document'].append(fileObj)