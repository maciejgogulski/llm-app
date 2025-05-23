import logging
import os
from flask import Blueprint, request, jsonify
from config.db_conf import execute, query

bp = Blueprint('documents', __name__, url_prefix='/documents')

LOG = logging.getLogger(__name__)
DOCUMENT_STORAGE_PATH = os.getenv('DOCUMENT_STORAGE_PATH', './uploads')

@bp.route('/', methods=['POST'])
def upload_document():
    LOG.info("Recieved upload-document request")
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        LOG.info(f"Saving file: {uploaded_file.filename}")
        save_path = f"{DOCUMENT_STORAGE_PATH}/{uploaded_file.filename}"
        uploaded_file.save(save_path)

        try:
            execute("""
                  INSERT INTO documents
                  (filename, filepath)
                  VALUES
                  (%(filename)s, %(filepath)s)
                """, 
                {
                      "filename": uploaded_file.filename,
                      "filepath": save_path
                }
            )
        except Exception as ex: 
            LOG.error(f"DB error occured: {ex}")
            
            return "DB error", 500
        
        return f"Saved to {save_path}", 200
    return "Invalid file", 400

@bp.route('/', methods=['GET'])
def get_documents():
    try:
        documents = query("""
            SELECT filename, 
                filepath, 
                DATE_FORMAT(added_at, '%Y-%m-%d %H:%i:%s') AS added_at,
                DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at
            FROM documents
        """)
    except Exception as ex:
        LOG.error(f"DB error occured: {ex}")
        return "DB error", 500

    return jsonify(documents)
