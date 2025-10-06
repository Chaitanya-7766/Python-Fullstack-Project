import streamlit as st
import requests

API_URL = "https://python-fullstack-project-1.onrender.com"

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------ LOGIN PAGE ------------------
def login_page():
    st.title("🔐 Login to Student Record System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        USERS = {"admin": "1234", "user1": "abcd"}  # example users
        if username in USERS and password == USERS[username]:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Login Successful! Welcome {username}")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Try again.")

# ------------------ HELPER FUNCTIONS ------------------
def safe_json_response(res):
    try:
        return res.json()
    except:
        return {"error": f"Non-JSON response: {res.text}"}

def get_students():
    res = requests.get(f"{API_URL}/students")
    data = safe_json_response(res)
    return data.get("data", [])

def add_student(name, age, branch, year, gpa):
    res = requests.post(f"{API_URL}/students", json={
        "name": name, "age": age, "branch": branch, "year": year, "gpa": gpa
    })
    return safe_json_response(res)

def update_student(student_id, gpa):
    res = requests.put(f"{API_URL}/students/{student_id}", json={"gpa": gpa})
    return safe_json_response(res)

def delete_student(student_id):
    res = requests.delete(f"{API_URL}/students/{student_id}")
    return safe_json_response(res)

# ------------------ MAIN APP ------------------
def main_app():
    st.sidebar.success(f"Welcome, {st.session_state.username} 👋")
    if st.sidebar.button("Refresh"):
        st.experimental_rerun()

    st.title("📚 Student Record System")

    menu = ["View Students", "Add Student", "Update Student GPA", "Delete Student", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Students":
        st.subheader("All Students")
        students = get_students()
        if students:
            st.table(students)
        else:
            st.write("No student records available.")

    elif choice == "Add Student":
        st.subheader("Add Student")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        branch = st.text_input("Branch")
        year = st.number_input("Year", min_value=1, max_value=8)
        gpa = st.number_input("GPA", min_value=0.0, max_value=10.0, step=0.01)
        if st.button("Add"):
            result = add_student(name, age, branch, year, gpa)
            st.success(result.get("message", result.get("error", "Error adding student")))

    elif choice == "Update Student GPA":
        st.subheader("Update Student GPA")
        student_id = st.number_input("Student ID", min_value=1, step=1)
        gpa = st.number_input("New GPA", min_value=0.0, max_value=10.0, step=0.01)
        if st.button("Update"):
            result = update_student(student_id, gpa)
            st.success(result.get("message", result.get("error", "Error updating student")))

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        student_id = st.number_input("Student ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            result = delete_student(student_id)
            st.success(result.get("message", result.get("error", "Error deleting student")))

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully!")
        st.experimental_rerun()

# ------------------ APP FLOW ------------------
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
