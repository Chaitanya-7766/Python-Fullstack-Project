import streamlit as st
import requests

API_URL = "https://python-fullstack-project-1.onrender.com"  # change to your Render backend

# -------- Safe JSON Response --------
def safe_json_response(res):
    try:
        return res.json()
    except Exception:
        return {"error": f"Non-JSON response: {res.text}", "status": res.status_code}

# -------- API Calls --------
def register(username, password):
    res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    return safe_json_response(res)

def login(username, password):
    res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return safe_json_response(res)

def get_students():
    res = requests.get(f"{API_URL}/students")
    return safe_json_response(res)

def add_student(name, age, branch, year, gpa):
    res = requests.post(f"{API_URL}/students", json={
        "name": name, "age": age, "branch": branch, "year": year, "gpa": gpa
    })
    return safe_json_response(res)

def update_student(student_id, gpa):
    res = requests.put(f"{API_URL}/students/{student_id}", json={"name":"", "age":0, "branch":"", "year":0, "gpa":gpa})
    return safe_json_response(res)

def delete_student(student_id):
    res = requests.delete(f"{API_URL}/students/{student_id}")
    return safe_json_response(res)

# -------- Session --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# -------- UI --------
st.sidebar.title("Authentication")

if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Choose Action", ["Login", "Register"])

    if choice == "Register":
        st.title("Register")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Register"):
            result = register(user, pw)
            if "User registered successfully" in result.get("message", ""):
                st.success("Registration successful. Please login.")
            else:
                st.error(result.get("detail", result.get("error", "Error registering user.")))

    elif choice == "Login":
        st.title("Login")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login(user, pw)
            if "Login successful" in result.get("message", ""):
                st.session_state.logged_in = True
                st.session_state.username = user
                st.success("Logged in successfully!")
            else:
                st.error(result.get("detail", result.get("error", "Login failed")))

else:
    st.sidebar.success(f"Welcome, {st.session_state.username} 👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

    # --- Student Manager UI ---
    st.title("📚 Student Record System")

    menu = ["View Students", "Add Student", "Update Student", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Students":
        st.subheader("All Students")
        students = get_students()
        if isinstance(students, list):
            st.table(students)
        else:
            st.write(students)

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

    elif choice == "Update Student":
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
