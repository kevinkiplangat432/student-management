# in this file  i import fast Api and route modules.
# routes modules are impported to registyer them with app.


from fastapi import FastAPI
from app.api.routes import auth, users, enrollment

#handle http requests.
app = FastAPI(title="Student Management System API") # create a Fast APIinstance

#register route modules with the app.
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"]) 
app.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def root():
    return {"message": "Student Management Backend Running"}

#study:
# include_router() connect each module's route to the main app.
# app.include_router
# (auth.router
# , prefix="/auth", this means all routes in auth.router will start with /auth 
# tags=["Auth"]) this syntax groups these endpoints in the auto generated APi docs