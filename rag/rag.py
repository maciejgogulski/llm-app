import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH')
MODEL = os.getenv('MODEL')
EMBEDDING_MODEL = OllamaEmbeddings(model="nomic-embed-text")
LOG = logging.getLogger(__name__)

def load_pdf(document_filename):
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
    chunks = chunk_data(load_pdf("sprawozdanie.pdf"))

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

