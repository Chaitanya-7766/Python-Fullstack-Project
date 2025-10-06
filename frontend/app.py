import streamlit as st
import requests

API_URL = "http://localhost:8080"   # change to Render backend URL after deployment

# -------- API Calls --------
def register(username, password):
    res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    return res.json()

def login(username, password):
    res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    return res.json()

def get_students():
    res = requests.get(f"{API_URL}/students")
    return res.json()

def add_student(name, age, grade):
    res = requests.post(f"{API_URL}/students", json={"name": name, "age": age, "grade": grade})
    return res.json()

def update_student(student_id, name, age, grade):
    res = requests.put(f"{API_URL}/students/{student_id}", json={"name": name, "age": age, "grade": grade})
    return res.json()

def delete_student(student_id):
    res = requests.delete(f"{API_URL}/students/{student_id}")
    return res.json()

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
                st.error(result.get("detail", "Error registering user."))

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
                st.error(result.get("detail", "Login failed"))

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
        st.write(students)

    elif choice == "Add Student":
        st.subheader("Add Student")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        grade = st.text_input("Grade")
        if st.button("Add"):
            result = add_student(name, age, grade)
            st.success(result["message"])

    elif choice == "Update Student":
        st.subheader("Update Student")
        student_id = st.number_input("Student ID", min_value=1, step=1)
        name = st.text_input("New Name")
        age = st.number_input("New Age", min_value=1, max_value=120)
        grade = st.text_input("New Grade")
        if st.button("Update"):
            result = update_student(student_id, name, age, grade)
            st.success(result["message"])

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        student_id = st.number_input("Student ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            result = delete_student(student_id)
            st.success(result["message"])
