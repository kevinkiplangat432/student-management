from fastapi import APIRouter, Depends, HTTPException # depends for dependency injection and httpException for http errors

from sqlalchemy.orm import Session
from app.db.models import Student, Course, enrollments_table
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.db.sessions import get_db

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

# Enroll a student in a course
@router.post("/", response_model=EnrollmentRead) # handle post request here and use EnrollmentRead to validate response

#validate against the EnrollmentCreate schema and inject database session
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db)):
    # query the database for  students and course
    student = db.query(Student).filter(Student.id == data.student_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()
    
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    if course in student.courses:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")
    
    student.courses.append(course)
    db.commit()
    return data

# Remove a student from a course
# handle delete request here
@router.delete("/", response_model=EnrollmentRead)

def remove_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db)):
    
    student = db.query(Student).filter(Student.id == data.student_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()
    
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    if course not in student.courses:
        raise HTTPException(status_code=400, detail="Student not enrolled in this course")
    
    student.courses.remove(course)
    db.commit()
    return data

# List all courses for a student
@router.get("/student/{student_id}", response_model=list[int])

def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return [course.id for course in student.courses]

# List all students in a course
@router.get("/course/{course_id}", response_model=list[int])
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return [student.id for student in course.students]
