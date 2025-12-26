import sqlite3

conn = sqlite3.connect("biopass.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS outing_requests;")

cursor.execute("""
CREATE TABLE outing_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_email TEXT,
    reason TEXT,
    out_time TEXT,
    expected_return TEXT,
    status TEXT,
    request_time TEXT,
    otp TEXT
);
""")

conn.commit()
conn.close()
print("[OK] outing_requests table recreated successfully.")
