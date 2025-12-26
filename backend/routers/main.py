from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import student, parent, faculty, security
from database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount folders
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/student_faces", StaticFiles(directory="student_faces"), name="student_faces")  # ✅ Mount this

# Initialize DB
init_db()

# Include Routers
app.include_router(student.router, prefix="/student")
app.include_router(parent.router, prefix="/parent")
app.include_router(faculty.router, prefix="/faculty")
app.include_router(security.router, prefix="/security")