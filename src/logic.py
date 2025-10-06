from src import db

class StudentManager:
    '''
    Acts as a bridge between frontend (Streamlit/FastAPI) and the database.
    '''

    # --- Create ------
    def add_student(self, name, age, branch, year, gpa):
        '''
        Add a new student to the database
        Return success message if the student is added
        '''
        if not name or not age or not branch or not year:
            return {"Success": False, "message": "name, age, branch, year are required"}
        
        result = db.create_student(name, age, branch, year, gpa)

        if result.data:
            return {"Success": True, "message": "Student added successfully", "student": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
    
    # --- Read ------
    def get_students(self):
        '''
        Get all the students from the database
        '''
        result = db.get_all_students()
        return result.data if result.data else "No Student record to display"
    
    # --- Update GPA ------
    def update_student_gpa(self, student_id, gpa):

        result = db.update_student(student_id, gpa)   # ✅ pass gpa directly, not dict
        if result.data:
            return {"Success": True, "message": "Student GPA updated successfully", "student": result.data}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}

    
    # --- Delete ------
    def delete_student(self, student_id):
        '''
        Delete a student from the database
        '''
        result = db.delete_student(student_id)
        if result.data:
            return {"Success": True, "message": "Student deleted successfully"}
        else:
            return {"Success": False, "message": f"Error: {result.error}"}
