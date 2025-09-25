# Frontend ----> API ----> logic ----> db ----> Response
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Add src to path to import StudentManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import StudentManager

# ------------------------------- App Setup ----------
app = FastAPI(title="Student Record System API", version="1.0")

# ------------------------------- CORS Middleware ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontend apps
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------------------- Student Manager Instance ----------
student_manager = StudentManager()  # create instance

# ------------------------------- Data Models ----------
class StudentCreate(BaseModel):
    name: str
    age: int
    branch: str
    year: int
    gpa: float

class StudentGPAUpdate(BaseModel):
    gpa: float

# ------------------------------- API Endpoints ----------

@app.get("/")
def home():
    """Check if API is running"""
    return {"message": "Student Record System API is running"}

@app.get("/students")
def get_students():
    """Get all students"""
    result = student_manager.get_students()
    return result

@app.post("/students")
def create_student(student: StudentCreate):
    """Add a new student"""
    result = student_manager.add_student(
        student.name, student.age, student.branch, student.year, student.gpa
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/students/{student_id}/gpa")
def update_student_gpa(student_id: int, student: StudentGPAUpdate):
    """Update a student's GPA"""
    result = student_manager.update_student_gpa(student_id, student.gpa)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """Delete a student"""
    result = student_manager.delete_student(student_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ------------------------------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
