import os
import shutil
import random
from datetime import datetime
from fastapi import APIRouter, Form, HTTPException, UploadFile, File, Request

from ..database import get_db_connection

router = APIRouter()

UPLOAD_FOLDER = "student_faces"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- STUDENT SIGNUP --------------------
@router.post("/signup")
async def student_signup(
    name: str = Form(...),
    roll_no: str = Form(...),
    branch: str = Form(...),
    email: str = Form(...),
    parent_phone: str = Form(...),
    password: str = Form(...),
    face: UploadFile = File(...)
):
    email = email.strip().lower()

    face_path = os.path.join(UPLOAD_FOLDER, face.filename)
    with open(face_path, "wb") as buffer:
        shutil.copyfileobj(face.file, buffer)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, roll_no, branch, email, parent_phone, password, face_filename)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, roll_no, branch, email, parent_phone, password, face.filename))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    conn.close()
    return {"message": "Student signup successful!"}


# -------------------- STUDENT LOGIN --------------------
@router.post("/login")
async def student_login(
    email: str = Form(...),
    password: str = Form(...)
):
    email = email.strip().lower()
    password = password.strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE email=? AND password=?", (email, password))
    student = cursor.fetchone()
    conn.close()

    if not student:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "student": {
            "name": student[1],
            "roll_no": student[2],
            "branch": student[3],
            "email": student[4],
        }
    }


# -------------------- OUTING REQUEST (FORM SUBMIT) --------------------
@router.post("/request-permission")
async def request_permission(
    email: str = Form(...),
    reason: str = Form(...),
    from_time: str = Form(...),
    to_time: str = Form(...)
):
    # Step 1: Connect to DB
    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 2: Get student_id using email
    cursor.execute("SELECT id FROM students WHERE email=?", (email,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    student_id = student[0]
    otp = "7195"  # Using default OTP for parent verification

    # Step 3: Insert outing request
    try:
        cursor.execute("""
            INSERT INTO outing_requests (
                student_id,
                student_email,
                reason,
                out_time,
                expected_return,
                status,
                request_time,
                otp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            email,
            reason,
            from_time,
            to_time,
            "Submitted",
            datetime.now(),
            otp
        ))
        conn.commit()
        conn.close()
        return {"message": "Outing request submitted successfully."}
    
    except Exception as e:
        print("❌ Database error:", e)  # <-- This shows you the real reason in terminal
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
# -------------------- STATUS CHECK --------------------
@router.get("/status")
def get_status(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status FROM outing_requests
        WHERE student_email = ?
        ORDER BY id DESC LIMIT 1
    """, (email,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"status": row[0]}
    else:
        return {"status": "No request found"}


# -------------------- OTP VERIFICATION --------------------
@router.post("/parent/verify-otp")
async def verify_otp(request: Request):
    data = await request.json()
    email = data["email"]
    entered_otp = data["otp"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT otp FROM outing_requests
        WHERE student_email = ? AND status = 'Submitted'
        ORDER BY id DESC LIMIT 1
    """, (email,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No request found")

    real_otp = row[0]
    if entered_otp == real_otp:
        cursor.execute("""
            UPDATE outing_requests
            SET status = 'Parent Accepted'
            WHERE student_email = ? AND status = 'Submitted'
        """, (email,))
        conn.commit()
        conn.close()
        return {"message": "Parent OTP verified. Request approved by parent."}
    else:
        conn.close()
        raise HTTPException(status_code=401, detail="Incorrect OTP")
