from fastapi import APIRouter, Form, HTTPException
from ..database import get_db_connection

router = APIRouter()

# Show all outing requests where parent has accepted
@router.get("/pending-requests")
def get_pending_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, student_email, reason, out_time, expected_return 
        FROM outing_requests
        WHERE status = 'Parent Accepted'
        ORDER BY request_time DESC
    """)
    requests = cursor.fetchall()
    conn.close()

    return {
        "requests": [
            {
                "id": r[0],
                "email": r[1],
                "reason": r[2],
                "from": r[3],
                "to": r[4]
            } for r in requests
        ]
    }

# Faculty decision endpoint
@router.post("/approve")
def approve_request(id: int = Form(...), decision: str = Form(...)):
    if decision not in ["Faculty Approved", "Faculty Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid decision")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE outing_requests SET status = ? WHERE id = ?", (decision, id))
    conn.commit()
    conn.close()

    return {"message": f"Request {decision.lower()} successfully"}
