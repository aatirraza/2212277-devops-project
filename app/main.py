from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, Field
import models
from database import get_db

app = FastAPI(title="DevOps Microservice Capstone")

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    reg_no: str = Field(..., min_length=3, max_length=20)
    class Config:
        from_attributes = True

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "ok", "db": db_status, "student": "2212277"}

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.reg_no == student.reg_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already registered.")
    db_student = models.Student(name=student.name, reg_no=student.reg_no)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students", status_code=status.HTTP_200_OK)
def read_all_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.get("/students/{reg_no}", status_code=status.HTTP_200_OK)
def read_student_by_id(reg_no: str, db: Session = Depends(get_db)):
    target = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"Student profile '{reg_no}' not found.")
    return target
