from pydantic import BaseModel, EmailStr
from typing import List, Optional

class SimpleStudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class SimpleCourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class StudentWithCoursesResponse(SimpleStudentResponse):
    courses: List[SimpleCourseResponse] = []

class CourseWithStudentsResponse(SimpleCourseResponse):
    students: List[SimpleStudentResponse] = []