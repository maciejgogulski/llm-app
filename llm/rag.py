"""
Module containing functions necessary to perform Retrieval Augmented Generation. 
Responsible for orchestrating the process, fetching documents, interacting with embedding model and llm.
"""

import os
import logging
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from db.repo import fetch_documents

MODEL = os.getenv('MODEL', 'ollama3')
EMBEDDING_MODEL = OllamaEmbeddings(model=os.getenv('EMBEDDING_MODEL', 'nomic-embed-text'))
LOG = logging.getLogger(__name__)

def load_pdf(document_filename) -> List[Document]:
    LOG.debug(f"Loading file: {document_filename}")

    storage_path = os.getenv('DOCUMENT_STORAGE_PATH')
    if not storage_path:
        raise ValueError("DOCUMENT_STORAGE_PATH environment variable is not set")

    loader = PyPDFLoader(f"{storage_path}/{document_filename}")
    return loader.load()

def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100) # TODO Export to env variable.
    chunks = splitter.split_documents(documents)
    
    for chunk in chunks:
        print(chunk)

    return chunks

def load_all_documents(pdf_documents_rows):
    docs = []
    for pdf_row in pdf_documents_rows:
        docs.extend(load_pdf(pdf_row["filename"]))
    return docs

def vectorize_documents(chunks):
    return FAISS.from_documents(chunks, EMBEDDING_MODEL)

def build_qa_chain(model, vectorstore):
    return RetrievalQA.from_chain_type(
        llm=model,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

def run_chain(chain, prompt: str):
    return chain(prompt)

def perform_rag(prompt: str):
    docs = load_all_documents(fetch_documents())
    chunks = chunk_data(docs)
    vectorstore = vectorize_documents(chunks)
    chain = build_qa_chain(OllamaLLM(model=MODEL), vectorstore)
    return run_chain(chain, prompt)

