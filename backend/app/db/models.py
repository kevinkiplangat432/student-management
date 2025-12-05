
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

#all models will inherit from this Base
Base = declarative_base()

# Many-to-Many between Students and Courses withouth ORM just association
enrollments_table = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key = True, index=True)
    uid = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, default="student") # or admin
    email =Column(String, nullable=True, unique=True)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    courses = relationship(
        "Course",
        secondary=enrollments_table,
        back_populates="students"
    )

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    students = relationship(
        "Student",
        secondary=enrollments_table,
        back_populates="courses"
    )
