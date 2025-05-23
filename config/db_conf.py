import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def query(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or {})
        result = cursor.fetchall()
        return result
    finally:
        conn.close()

def execute(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or {})
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
