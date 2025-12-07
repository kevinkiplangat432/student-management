# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, students, courses, enrollment
from app.core.config import settings

app = FastAPI(
    title="Student Management System API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

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
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "cors_origins": settings.cors_origins
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "student-management-api"}