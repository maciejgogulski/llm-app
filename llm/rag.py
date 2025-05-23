import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from db.repo import fetch_documents

DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH')
MODEL = os.getenv('MODEL')
EMBEDDING_MODEL = OllamaEmbeddings(model=os.getenv('EMBEDDING_MODEL', 'nomic-embed-text'))
LOG = logging.getLogger(__name__)

def load_pdf(document_filename):
    LOG.debug(f"Loading file: {document_filename}")
    loader = PyPDFLoader(f"{DOCUMENT_STORAGE_PATH}/{document_filename}")
    return loader.load()

def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100) # TODO Export to env variable.
    chunks = splitter.split_documents(documents)
    
    for chunk in chunks:
        print(chunk)

    return chunks

def perform_rag(prompt):
    LOG.info("Performing RAG")

    pdf_documents_rows = fetch_documents()
    
    docs = []
    for pdf_row in pdf_documents_rows:
        docs.extend(load_pdf(pdf_row["filename"]))

    chunks = chunk_data(docs)

    vectorstore = FAISS.from_documents(chunks, EMBEDDING_MODEL)

    llm = Ollama(model=MODEL)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

    result = qa_chain(prompt)

    LOG.info(f"The result of RAG: {result}")
    
    return result

