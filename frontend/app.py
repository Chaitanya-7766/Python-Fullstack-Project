import streamlit as st
import requests

API_URL = "http://localhost:8080"  # Adjust if API is deployed elsewhere

st.set_page_config(page_title="Student Record System", layout="centered")
st.title("🎓 Student Record System")

# --------------------------------------------
# Helper functions to interact with the API
# --------------------------------------------

def get_students():
    try:
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch students.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def add_student(data):
    response = requests.post(f"{API_URL}/students", json=data)
    return response

def update_gpa(student_id, new_gpa):
    response = requests.put(f"{API_URL}/students/{student_id}/gpa", json={"gpa": new_gpa})
    return response

def delete_student(student_id):
    response = requests.delete(f"{API_URL}/students/{student_id}")
    return response

# --------------------------------------------
# Sidebar Navigation
# --------------------------------------------
st.sidebar.title("📋 Menu")
menu = st.sidebar.radio("Go to", ["View Students", "Add Student", "Update GPA", "Delete Student"])

# --------------------------------------------
# View Students
# --------------------------------------------
if menu == "View Students":
    st.subheader("📖 All Student Records")
    students = get_students()

    if isinstance(students, list) and students:
        st.dataframe(students, use_container_width=True)
    elif not students:
        st.info("No students found.")
    else:
        st.write(students)  # In case API returns string error

# --------------------------------------------
# Add Student
# --------------------------------------------
elif menu == "Add Student":
    st.subheader("➕ Add New Student")

    with st.form("add_student_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, step=1)
        branch = st.text_input("Branch")
        year = st.number_input("Year", min_value=1, step=1)
        gpa = st.number_input("GPA", min_value=0.0, max_value=10.0, step=0.1)
        submitted = st.form_submit_button("Add Student")

        if submitted:
            student_data = {
                "name": name,
                "age": age,
                "branch": branch,
                "year": year,
                "gpa": gpa
            }
            res = add_student(student_data)
            if res.status_code == 200:
                st.success("Student added successfully!")
            else:
                st.error(f"Failed to add student: {res.json().get('detail')}")

# --------------------------------------------
# Update GPA
# --------------------------------------------
elif menu == "Update GPA":
    st.subheader("🔄 Update Student GPA")

    students = get_students()
    if isinstance(students, list) and students:
        student_map = {f"{s['student_id']}: {s['name']}": s['student_id'] for s in students}
        selected = st.selectbox("Select Student", list(student_map.keys()))
        student_id = student_map[selected]
        new_gpa = st.number_input("New GPA", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Update GPA"):
            res = update_gpa(student_id, new_gpa)
            if res.status_code == 200:
                st.success("GPA updated successfully!")
            else:
                st.error(f"Error updating GPA: {res.json().get('detail')}")
    else:
        st.info("No students available to update.")

# --------------------------------------------
# Delete Student
# --------------------------------------------
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student")

    students = get_students()
    if isinstance(students, list) and students:
        student_map = {f"{s['student_id']}: {s['name']}": s['student_id'] for s in students}
        selected = st.selectbox("Select Student to Delete", list(student_map.keys()))
        student_id = student_map[selected]

        if st.button("Delete Student"):
            res = delete_student(student_id)
            if res.status_code == 200:
                st.success("Student deleted successfully!")
            else:
                st.error(f"Failed to delete student: {res.json().get('detail')}")
    else:
        st.info("No students to delete.")
