from pydantic import BaseModel, EmailStr
from typing import List, Optional   

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  

class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    courses: List["CourseResponse"] = []

    class Config:
        from_attribute = True


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    students: List[StudentResponse] = []

    class Config:
        from_attributes = True

StudentResponse.update_forward_refs()
