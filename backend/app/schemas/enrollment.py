from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentRead(BaseModel):
    student_id: int
    course_id: int

    class Config:
        from_attributes = True
