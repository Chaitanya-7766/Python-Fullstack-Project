import streamlit as st
import requests

API_URL = "https://python-fullstack-project-1.onrender.com"  # your backend URL

# -------- Safe JSON Response --------
def safe_json_response(res):
    try:
        return res.json()
    except Exception:
        return {"error": f"Non-JSON response: {res.text}", "status": res.status_code}

# -------- API Calls --------
def get_students():
    res = requests.get(f"{API_URL}/students")
    data = safe_json_response(res)
    # Ensure we get a list for st.table
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data

def add_student(name, age, branch, year, gpa):
    res = requests.post(f"{API_URL}/students", json={
        "name": name, "age": age, "branch": branch, "year": year, "gpa": gpa
    })
    return safe_json_response(res)

def update_student(student_id, gpa):
    # Only GPA update
    res = requests.put(f"{API_URL}/students/{student_id}", json={
        "gpa": gpa
    })
    return safe_json_response(res)

def delete_student(student_id):
    res = requests.delete(f"{API_URL}/students/{student_id}")
    return safe_json_response(res)

# -------- Session State --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN PAGE --------
def login_page():
    st.title("Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "chaitanya" and pw == "chai123":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

# -------- STUDENT MANAGEMENT PAGE --------
def student_page():
    st.sidebar.success("Welcome, chaitanya 👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    st.title("📚 Student Record System")

    menu = ["View Students", "Add Student", "Update Student GPA", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    # ----- View Students -----
    if choice == "View Students":
        st.subheader("All Students")
        students = get_students()
        if isinstance(students, list) and students:
            st.table(students)
        else:
            st.write("No student records available.")

    # ----- Add Student -----
    elif choice == "Add Student":
        st.subheader("Add Student")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        branch = st.text_input("Branch")
        year = st.number_input("Year", min_value=1, max_value=8)
        gpa = st.number_input("GPA", min_value=0.0, max_value=10.0, step=0.01)

        if st.button("Add"):
            result = add_student(name, age, branch, year, gpa)
            if "message" in result:
                st.success(result["message"])
            else:
                st.error(result.get("error", "Error adding student"))

    # ----- Update Student GPA -----
    elif choice == "Update Student GPA":
        st.subheader("Update Student GPA")
        student_id = st.number_input("Student ID", min_value=1, step=1)
        gpa = st.number_input("New GPA", min_value=0.0, max_value=10.0, step=0.01)
        if st.button("Update"):
            result = update_student(student_id, gpa)
            if "message" in result:
                st.success(result["message"])
            else:
                st.error(result.get("error", "Error updating student"))

    # ----- Delete Student -----
    elif choice == "Delete Student":
        st.subheader("Delete Student")
        student_id = st.number_input("Student ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            result = delete_student(student_id)
            if "message" in result:
                st.success(result["message"])
            else:
                st.error(result.get("error", "Error deleting student"))

# -------- MAIN --------
if st.session_state.logged_in:
    student_page()
else:
    login_page()
