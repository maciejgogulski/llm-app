import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/llm")
DOCUMENTS_API_URL = API_BASE_URL.replace("/llm", "/documents")  # assumes same host/port

st.set_page_config(page_title="Document Manager", layout="centered")
st.title("📄 Document Management for RAG")

# ---- Upload Section ----
st.subheader("Upload PDF Document")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    if st.button("Upload"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{DOCUMENTS_API_URL}/", files=files)
            if response.status_code == 200:
                st.success(f"Uploaded: {uploaded_file.name}")
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"An error occurred during upload: {e}")

# ---- List Section ----
st.subheader("Available Documents")

try:
    response = requests.get(f"{DOCUMENTS_API_URL}/")
    if response.status_code == 200:
        documents = response.json()
        if documents:
            for doc in documents:
                st.write(f"📎 {doc['filename']}")
        else:
            st.info("No documents found.")
    else:
        st.error(f"Failed to fetch documents: {response.text}")
except Exception as e:
    st.error(f"An error occurred while fetching documents: {e}")
