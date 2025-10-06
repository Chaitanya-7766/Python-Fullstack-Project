from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.logic import StudentManager

app = FastAPI()
student_manager = StudentManager()

# --- Models ---
class Student(BaseModel):
    name: str
    age: int
    branch: str
    year: int
    gpa: float

# ---------------- STUDENTS ----------------
@app.get("/")
def root():
    return {"message": "Student Record System API is running"}

@app.get("/students")
def get_students():
    return student_manager.get_students()

@app.post("/students")
def add_student(student: Student):
    result = student_manager.add_student(
        student.name, student.age, student.branch, student.year, student.gpa
    )
    if result["Success"]:
        return {"message": result["message"]}
    raise HTTPException(status_code=400, detail=result["message"])

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    result = student_manager.update_student_gpa(student_id, student.gpa)
    if result["Success"]:
        return {"message": result["message"]}
    raise HTTPException(status_code=400, detail=result["message"])

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    result = student_manager.delete_student(student_id)
    if result["Success"]:
        return {"message": result["message"]}
    raise HTTPException(status_code=400, detail=result["message"])
