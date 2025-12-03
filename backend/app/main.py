from fastapi import FastAPI
from app.api.routes import auth, users  

app = FastAPI(title="Student Management System API")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"]) 

@app.get("/")
def root():
    return {"message": "Student Management Backend Running"}
