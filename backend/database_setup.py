import sqlite3

conn = sqlite3.connect("biopass.db")
cursor = conn.cursor()

# Students table
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

# Outing requests table
cursor.execute("""
CREATE TABLE IF NOT EXISTS outing_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    reason TEXT,
    from_time TEXT,
    to_time TEXT,
    parent_status TEXT DEFAULT 'Pending',
    faculty_status TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()
