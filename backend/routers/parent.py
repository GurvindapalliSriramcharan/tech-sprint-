from fastapi import APIRouter, Form, HTTPException
from ..database import get_db_connection

router = APIRouter()

DEFAULT_OTP = "7195"

@router.post("/verify-otp")
async def verify_otp(student_email: str = Form(...), otp: str = Form(...)):
    if otp != DEFAULT_OTP:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Get the latest request ID for that email
    cursor.execute("SELECT id FROM outing_requests WHERE student_email = ? ORDER BY id DESC LIMIT 1", (student_email,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="No outing request found for this email")

    request_id = row["id"]

    # Step 2: Update the parent_status for that specific request
    cursor.execute("UPDATE outing_requests SET status = 'Parent Accepted' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

    return {"message": "OTP verified and parent approved"}
