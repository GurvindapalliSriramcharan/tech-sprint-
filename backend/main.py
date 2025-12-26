import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import init_db
from .routers import student, parent, faculty, security


app = FastAPI()


# Enable CORS so HTML/JS can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables
init_db()


# Include Routers
app.include_router(student.router, prefix="/student")
app.include_router(parent.router, prefix="/parent")
app.include_router(faculty.router, prefix="/faculty")
app.include_router(security.router, prefix="/security")

# Serve static files from the frontend directory
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
