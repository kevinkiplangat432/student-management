# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, students, courses, enrollment
from app.core.config import settings
import os

# Import database models and engine
from app.db.models import Base
from app.db.sessions import engine

app = FastAPI(
    title="Student Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# Include routers
app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"]) 
app.include_router(students.router, tags=["Students"])  
app.include_router(courses.router, tags=["Courses"])
app.include_router(enrollment.router, tags=["Enrollments"])

@app.get("/")
def root():
    return {
        "message": "Student Management Backend Running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "student-management-api"}

@app.get("/debug")
def debug_info():
    return {
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "pg_host": bool(os.getenv("PGHOST")),
        "firebase_creds": bool(os.getenv("FIREBASE_CREDENTIALS")),
        "debug_mode": os.getenv("DEBUG"),
        "message": "Database tables should be created on startup"
    }