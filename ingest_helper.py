import os,uuid
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import llm_helper,pymilvus_db_helper
import streamlit as st

COLLECTION_NAME = st.secrets["DB_COLLECTION_NAME"]  # Set your collection name

def proccess_pdf(file):
    loader = PyPDFLoader(file)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap=100)
    documents = text_splitter.split_documents(data)
    texts = [doc.page_content for doc in documents]
    return texts

def add_document(file):
    file_name = os.path.basename(file) 
    texts = proccess_pdf(file)
    texts_embeddings = llm_helper.create_embeddings(texts)
    i = 1
    data_list = []
    for text,text_embedding in zip(texts,texts_embeddings):
        id = f"{file_name}_{i}"
        data={      "title": file_name, 
                    "text": text,
                    "namespace" : file_name,
                    "vector": text_embedding }
        data_list.append(data)
        i += 1
    res = pymilvus_db_helper.insert(data_list,COLLECTION_NAME)

if __name__ == '__main__':
    add_document("dragon_ball.pdf")