import logging
import os
from flask import Blueprint, request, jsonify
import db.repo as repo
import hashlib

bp = Blueprint('documents', __name__, url_prefix='/documents')

LOG = logging.getLogger(__name__)
DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH', './uploads')

def compute_checksum(file_storage_obj):
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file_storage_obj.stream.read(4096), b""):
        hasher.update(chunk)
    file_storage_obj.stream.seek(0)
    return hasher.digest()

@bp.route('/', methods=['POST'])
def upload_document_route():
    LOG.info("Received upload_document request")
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        LOG.info(f"Processing file: {uploaded_file.filename}")

        # Compute checksum
        checksum = compute_checksum(uploaded_file)

        # Check for duplicates
        if repo.document_exists_by_checksum(checksum):
            LOG.info("Duplicate document detected, skipping save.")
            return "Duplicate document", 409  # Conflict

        save_path = os.path.join(DOCUMENT_STORAGE_PATH, uploaded_file.filename)
        uploaded_file.save(save_path)

        try:
            repo.insert_document(uploaded_file.filename, save_path, checksum)
        except Exception as ex:
            LOG.error(f"DB error occurred: {ex}")
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


