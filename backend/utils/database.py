import sqlite3

def get_db_connection():
    conn = sqlite3.connect("C:/Users/srira/Downloads/BIO-PASS_FULL_SYSTEM/backend/biopass.db")  # FULL PATH
    conn.row_factory = sqlite3.Row
    return conn