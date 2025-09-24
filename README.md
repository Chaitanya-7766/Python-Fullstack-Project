# Student Record Management

Student Record System is a simple Python project using Supabase that allows adding, viewing, updating, and deleting student details like name, age, branch, year, and GPA. It helps manage student data efficiently with a single database table.

## Core Features
**Add Student**
Register a new student with details like name, age, branch, year, and GPA.
**View Students**
Display all students stored in the database.
**Search Student**
Find a student by ID, branch, or year.
**Update GPA**
Modify a student’s GPA or other details.
**Delete Student**
Remove a student’s record from the system.
## Optional / Advanced Features
**List Toppers**
Show students with the highest GPA.
**Filter Students**
List students by branch, year, or GPA range.
**Data Persistence**
Store all student data in a database (Supabase/PostgreSQL).
**Report Generation** 
Export student data in CSV or PDF format.
**Authentication**
Admin login to manage records securely.

# Project Structure
StudentRecordManagement/
|
|----src/                   #core application logic
|    |--logic.py            #Business logic and task
|    |--db.py               #Database operations
|
|----api/                   #Backend API
|    |--main.py             #FastAPI endpoints
|
|----frontend/              #Frontend application
|    |--app.py              #Streamlit with web interface
|
|____requirements.txt       #Python dependencies
|
|____README.md              #Project Documentation
|
|____.env                   #Python variables

## Prerequisites
-Python 3.8 or above
-A supabase account
-Git(Push,Cloning)

## 1. Clone or Download the Project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2. Download and extract the ZIP file

## 2. Install Dependencies

# Install all required Python Packages
pip install -r requirements.txt

## 3. Set up supabase Database

1.Create a supabase project: 

2.Create the Tasks table:

-Go to SQL Editor in your supabase dashboard

-Run this SQL command:

```sql
CREATE TABLE students (
    student_id serial PRIMARY KEY,
    name text NOT NULL,
    age int NOT NULL,
    branch text NOT NULL,
    year int NOT NULL,
    gpa numeric
);

```

3.Get your credentials

## 4. Configure environmental variables

1. Create a `.env` file in the project root

2. Add your supabase credentials to `.env`:
    SUPABASE_URL=your_project_url
    SUPABASE_KEY=your_project_key

-**example**
SUPABASE_URL = https://xntagxcagezzncqnqxkb.supabase.co
SUPABASE_KEY = yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhudGFneGNhZ2V6em5jcW5xeGtiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIzMTAsImV4cCI6MjA3MzY1ODMxMH0.-BiPqlT23VNLfdeO5SiTeScHiQfdptN7BzoQk6120so

## 5. Run the application

## Streamlit frontend
streamlit run frontend/app.py

the app will open in your browser at `http://localhost:8000`

## how to use

## Technical details

## Techonologies used
-**Frontend**: Streamlit (Python web framework)
-**Backend**: FastAPI(Python REST API Framework)
-**Database**: supabase(PostgresSQL-based-Backend-as-a-service)
-**Language**: python 3.8+

## Key Components
 
1. **`src/db.py`**: Database operations 
    -Handles all CRUD operations with supabase

2. **src/logic.py`**: Buisiness logic
    -Task validation and processing

## Troubleshooting

## common issues

## Future Enchancements

## support

If you encounter any issues or have questions:
Phone no.: +91 9381744288
Email: saichaitanyav05@gmail.com