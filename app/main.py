from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from database import engine, get_db

# Automatically build relational structural database schemas upon load
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Microservice Capstone")

# Pydantic input schemas to parse arriving client data structures safely
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    reg_no: str = Field(..., min_length=3, max_length=20)

    class Config:
        orm_mode = True

# 1. GET /health (Crucial individual verification requirement)
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database execution sanity dynamically
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
        
    return {
        "status": "ok",
        "db": db_status,
        "student": "2212277"  # Your exact registration ID verified
    }

# 2. POST /students (Create single student record)
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if entry already exists to avoid structural uniqueness errors
    existing_student = db.query(models.Student).filter(models.Student.reg_no == student.reg_no).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this registration number already registered."
        )
    
    db_student = models.Student(name=student.name, reg_no=student.reg_no)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# 3. GET /students (List all student records)
@app.get("/students", status_code=status.HTTP_200_OK)
def read_all_students(db: Session = Depends(get_db)):
    students_list = db.query(models.Student).all()
    return students_list

# 4. GET /students/{reg_no} (Find specific student profile data)
@app.get("/students/{reg_no}", status_code=status.HTTP_200_OK)
def read_student_by_id(reg_no: str, db: Session = Depends(get_db)):
    target_student = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if not target_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student profile with registration query '{reg_no}' not found."
        )
    return target_student
