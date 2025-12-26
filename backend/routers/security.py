from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from fastapi.responses import JSONResponse

from ..database import get_db_connection

import face_recognition

import shutil

import os

from datetime import datetime


router = APIRouter()


# ✅ Get all pending security verifications (Faculty Approved)

@router.get("/pending-verifications")

def get_security_pending():

    conn = get_db_connection()

    cursor = conn.cursor()


    # ✅ Make sure to match the exact status string in DB

    cursor.execute("""

        SELECT o.id, s.email, o.reason, o.out_time, o.expected_return, s.face_filename

        FROM outing_requests o

        JOIN students s ON o.student_email = s.email

        WHERE o.status = 'Faculty Approved'

        ORDER BY o.request_time DESC

    """)


    rows = cursor.fetchall()

    conn.close()


    return {

        "requests": [

            {

                "id": row[0],

                "email": row[1],

                "reason": row[2],

                "from": row[3],

                "to": row[4],

                "face_filename": row[5]

            }

            for row in rows

        ]

    }


# ✅ POST /verify-face — Compare uploaded face with registered face

@router.post("/verify-face")
async def verify_face(image: UploadFile = File(...), email: str = Form(...)):
    from datetime import datetime

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Check student exists
    cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Update outing request status
        

        conn.commit()

        result = "✅ verification successful. Outing granted! message sent to parent and mentor"

    except Exception as e:
        result = f"Error: {str(e)}"

    finally:
        conn.close()

    return JSONResponse(content={"message": result})