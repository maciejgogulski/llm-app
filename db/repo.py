from config.db_conf import execute, query
from typing import List, Dict, Any, Optional

def insert_document(filename, filepath):
    execute("""
            INSERT INTO documents
                (filename, filepath)
            VALUES
                (%(filename)s, %(filepath)s)
        """, 
        {
            "filename": filename,
            "filepath": filepath
        }
    )

def fetch_documents() -> List[Dict[str, Any]]:
    return query("""
            SELECT filename, 
                filepath, 
                DATE_FORMAT(added_at, '%Y-%m-%d %H:%i:%s') AS added_at,
                DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at
            FROM documents
        """
    )
