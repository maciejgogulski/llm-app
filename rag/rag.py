from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf():
    pass

def chunk_data(document_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(document_text)
    
    for chunk in chunks:
        print(chunk)

    return chunks
