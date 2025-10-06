import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def create_student(name, age, branch, year, gpa):
    return supabase.table("students").insert({
        "name": name, "age": age, "branch": branch, "year": year, "gpa": gpa
    }).execute()

def get_all_students():
    return supabase.table("students").select("*").order("year").execute()

def update_student(student_id, gpa):
    return supabase.table("students").update({"gpa": gpa}).eq("student_id", student_id).execute()

def delete_student(student_id):
    return supabase.table("students").delete().eq("student_id", student_id).execute()
