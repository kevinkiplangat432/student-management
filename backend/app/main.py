from fastapi import FastAPI
from app.api.routes import auth, users, courses,  enrollments, students

app = FastAPI(title="Student Management System API")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"]) 
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def root():
    return {"message": "Student Management Backend Running"}
