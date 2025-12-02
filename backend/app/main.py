from fastapi import FastAPI
from app.api.routes import auth

app = FastAPI(title="Student Management System API")

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Student Management Backend Running"}
