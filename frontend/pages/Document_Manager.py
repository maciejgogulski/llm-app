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
    if st.button("Upload", key="Upload"):
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

def handle_delete_file_button_click(filename):
    try:
        response = requests.delete(f"{DOCUMENTS_API_URL}/{filename}")
        if response.status_code == 200:
            st.success(f"{filename} deleted.")
            st.experimental_rerun()  # Refresh the page to reflect deletion
        else:
            raise Exception(response.text)
    except Exception as e:
        st.session_state[f"error_{filename}"] = str(e)

def handle_download_file_button_click(filename):
    try:
        r = requests.get(f"{DOCUMENTS_API_URL}/{filename}")
        r.raise_for_status()
        st.session_state.download_data[filename] = r.content
        st.experimental_rerun()
    except Exception as e:
        st.session_state[f"error_{filename}"] = str(e)


if "download_data" not in st.session_state:
    st.session_state.download_data = {}

try:
    response = requests.get(f"{DOCUMENTS_API_URL}/")
    if response.status_code == 200:
        documents = response.json()
        if documents:
            for doc in documents:
                col1, col2, col3, col4 = st.columns([6, 3, 3, 5])  # Adjust proportions as needed

                with col1:
                    st.markdown(f"📕 `{doc['filename']}`")

                with col2:
                    if st.button("⬇ Download", key=f"fetch_{doc['filename']}"):
                        handle_delete_file_button_click(doc['filename'])

                with col3:
                    if st.button("✖ Delete", key=f"del_{doc['filename']}"):
                        handle_delete_file_button_click(doc['filename'])

                with col4:
                    error_key = f"error_{doc['filename']}"
                    if error_key in st.session_state:
                        st.error(st.session_state[error_key])

                if doc['filename'] in st.session_state.download_data:
                    st.download_button(
                        label=f"Click here to download {doc['filename']}",
                        data=st.session_state.download_data[doc['filename']],
                        file_name=doc['filename'],
                        mime="application/pdf",
                        key=f"download_button_{doc['filename']}"
                    )
                    # Optionally remove from session after showing:
                    del st.session_state.download_data[doc['filename']]

        else:
            st.info("No documents found.")
    else:
        st.error(f"Failed to fetch documents: {response.text}")
except Exception as e:
    st.error(f"An error occurred while fetching documents: {e}")



