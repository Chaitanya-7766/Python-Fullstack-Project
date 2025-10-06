from src import db

class StudentManager:
    '''
    Acts as a bridge between frontend (Streamlit/FastAPI) and the Supabase database.
    '''

    def add_student(self, name, age, branch, year, gpa):
        if not name or not age or not branch or not year:
            return {"Success": False, "message": "name, age, branch, year are required"}
        result = db.create_student(name, age, branch, year, gpa)
        if result.data:
            return {"Success": True, "message": "Student added successfully", "student": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    def get_students(self):
        result = db.get_all_students()
        return result.data if result.data else []

    def update_student_gpa(self, student_id, gpa):
        result = db.update_student(student_id, gpa)
        if result.data:
            return {"Success": True, "message": "Student GPA updated successfully"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    def delete_student(self, student_id):
        result = db.delete_student(student_id)
        if result.data:
            return {"Success": True, "message": "Student deleted successfully"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
