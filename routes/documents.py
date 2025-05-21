import logging
import os
from flask import Blueprint, request

bp = Blueprint('documents', __name__, url_prefix='/documents')

LOG = logging.getLogger(__name__)
DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH', './uploads')

@bp.route('/upload-document', methods=['POST'])
def upload_document():
    LOG.info("Recieved upload-document request")
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        LOG.info(f"Saving file: {uploaded_file.filename}")
        save_path = f"{DOCUMENT_STORAGE_PATH}/{uploaded_file.filename}"
        uploaded_file.save(save_path)
        return f"Saved to {save_path}", 200
    return "Invalid file", 400
