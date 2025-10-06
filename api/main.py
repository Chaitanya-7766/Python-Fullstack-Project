from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from src.logic import StudentManager
from src.db import Database

# --- Initialize ---
app = FastAPI()
db = Database()
student_manager = StudentManager()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Models ---
class Student(BaseModel):
    name: str
    age: int
    branch: str
    year: int
    gpa: float

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# --- Setup User Table ---
db.execute_query("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ---------------- AUTH ----------------
@app.post("/register")
def register(user: UserRegister):
    hashed_pw = pwd_context.hash(user.password)
    try:
        db.execute_query(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_pw)
        )
        return {"message": "User registered successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login")
def login(user: UserLogin):
    row = db.fetch_one("SELECT * FROM users WHERE username = ?", (user.username,))
    if not row or not pwd_context.verify(user.password, row["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "username": user.username}

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
