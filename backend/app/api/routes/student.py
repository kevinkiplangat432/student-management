from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Student
from app.schemas.schemas import StudentCreate, StudentResponse
from app.db.sessions import get_db

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if student with email already exists
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_student = Student(name=student.name, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if email is being changed to an existing email
    if student_data.email != student.email:
        existing = db.query(Student).filter(Student.email == student_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    
    student.name = student_data.name
    student.email = student_data.email
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return {"detail": "Student deleted successfully"}