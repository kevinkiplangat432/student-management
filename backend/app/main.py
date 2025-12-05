# in this file  i import fast Api and route modules.
# routes modules are impported to registyer them with app.


from fastapi import FastAPI
from app.api.routes import auth, users, students, courses,enrollment

#handle http requests.
app = FastAPI(title="Student Management System API") # create a Fast APIinstance

#register route modules with the app.
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, tags=["Users"]) 
app.include_router(students.router, tags=["Students"])  
app.include_router(courses.router, tags=["Courses"])
app.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def root():
    return {"message": "Student Management Backend Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "student-management-api"}

#study:
# include_router() connect each module's route to the main app.
# app.include_router
# (auth.router
# , prefix="/auth", this means all routes in auth.router will start with /auth 
# tags=["Auth"]) this syntax groups these endpoints in the auto generated APi docs