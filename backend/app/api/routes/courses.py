from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Course
from app.db.sessions import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/courses", tags=["Courses"])

# Simple schemas defined right here
class CourseCreate(BaseModel):
    title: str
    description: str = ""

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True

# CREATE COURSE
@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(title=course.title, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# GET ALL COURSES
@router.get("/", response_model=List[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# GET SPECIFIC COURSE
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# UPDATE COURSE
@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int, 
    course_data: CourseCreate, 
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.title = course_data.title
    course.description = course_data.description
    db.commit()
    db.refresh(course)
    return course

# DELETE COURSE
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted successfully"}
