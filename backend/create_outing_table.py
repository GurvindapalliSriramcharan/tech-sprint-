import sqlite3

conn = sqlite3.connect("biopass.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS outing_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_email TEXT,
    reason TEXT,
    out_time TEXT,
    expected_return TEXT,
    from_time TEXT,
    to_time TEXT,
    status TEXT DEFAULT 'Submitted',
    request_time TEXT,
    otp TEXT,
    faculty_status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

conn.commit()
conn.close()

print("outing_requests table created successfully.")
