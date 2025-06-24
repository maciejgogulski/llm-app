from config.db_conf import execute, query
from typing import List, Dict, Any, Optional

def insert_document(filename, filepath, checksum):
    execute("""
            INSERT INTO documents
                (filename, filepath, checksum)
            VALUES
                (%(filename)s, %(filepath)s, %(checksum)s);
        """, 
        {
            "filename": filename,
            "filepath": filepath,
            "checksum": checksum
        }
    )

def fetch_documents() -> List[Dict[str, Any]]:
    return query("""
            SELECT filename, 
                filepath, 
                DATE_FORMAT(added_at, '%Y-%m-%d %H:%i:%s') AS added_at,
                DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at
            FROM documents
            WHERE deleted_at IS NULL;
        """
    )

def delete_document(filename):
    return execute("""
            UPDATE documents
                   SET deleted_at = CURRENT_TIMESTAMP()
            WHERE filename = %(filename)s;
        """,
        {
            "filename": filename
        }
    )

def document_exists_by_checksum(checksum_bytes) -> bool:
    sql = "SELECT 1 FROM documents WHERE checksum = %s LIMIT 1"
    result = query(sql, (checksum_bytes,))
    return bool(result)
