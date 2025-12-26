import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "biopass.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        branch TEXT,
        email TEXT UNIQUE,
        parent_phone TEXT,
        password TEXT,
        face_filename TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outing_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        reason TEXT,
        from_time TEXT,
        to_time TEXT,
        otp TEXT,
        parent_status TEXT DEFAULT 'Pending',
        faculty_status TEXT DEFAULT 'Pending'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("[OK] All tables ensured in database.")

init_db()
