import logging
import os
from flask import Blueprint, request, jsonify
import db.repo as repo

bp = Blueprint('documents', __name__, url_prefix='/documents')

LOG = logging.getLogger(__name__)
DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH', './uploads')

@bp.route('/', methods=['POST'])
def upload_document_route():
    LOG.info("Recieved upload_document request")
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        LOG.info(f"Saving file: {uploaded_file.filename}")
        save_path = f"{DOCUMENT_STORAGE_PATH}/{uploaded_file.filename}"
        uploaded_file.save(save_path)

        try:
            repo.insert_document(uploaded_file.filename, save_path)
            
        except Exception as ex: 
            LOG.error(f"DB error occured: {ex}")
            return "DB error", 500
        
        return f"Saved to {save_path}", 200
    return "Invalid file", 400

@bp.route('/', methods=['GET'])
def get_documents_route():
    LOG.info("Recieved get_documents request")
    try:
        documents = repo.fetch_documents()
    except Exception as ex:
        LOG.error(f"DB error occured: {ex}")
        return "DB error", 500

    return jsonify(documents)


@bp.route('/<filename>', methods=['DELETE'])
def delete_document_route(filename):
    LOG.info("Recieved delete_document request")
    try:
        repo.delete_document(filename)
    except Exception as ex: 
        LOG.error(f"DB error occured: {ex}")
        return "DB error", 500
        
    return f"Deleted document{filename}", 200


