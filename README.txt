========================================================
STUDENT GRADE MANAGEMENT SYSTEM
Database Principles and Applications – Final Project
========================================================

PROJECT NAME:
Student Grade Management System

========================================================
1. PROJECT DESCRIPTION
========================================================

This project is a complete Student Grade Management System 
developed as part of the Database Principles and Applications course.

The system allows management of:

- Student information
- Course information
- Course enrollment (many-to-many relationship)
- Grade entry and updates
- Transcript generation (GPA calculation)
- Grade distribution analysis
- Role-based access control (Admin, Teacher, Student)

The system is implemented using:
- SQL Server (Database)
- Flask (Backend API)
- HTML + Bootstrap + JavaScript (Frontend)

========================================================
2. SYSTEM ROLES
========================================================

The system supports three user roles:

1. ADMIN
   - Manage students, courses, enrollments, and grades
   - View full system statistics

2. TEACHER
   - View assigned courses
   - Manage grades
   - View student performance

3. STUDENT
   - View personal grades
   - View transcript
   - View enrolled courses

========================================================
3. PROJECT STRUCTURE
========================================================
/school_project
   app.py
   db.py
   test.py

/routes
    
    auth.py
    courses.py
    dashboard.py
    department.py
    enrollments.py
    grades.py
    stats.py
    students.py
    transcript.py
    

/utils
    auth.py


/frontend
    app.js
    courses.html
    dashboard.html
    department_ranking.html
    enrollments.html
    grades.html
    transcript.html
    grade_distribution.html
    login.html
    students.html
    transcript.html

	/components
    	   header.js

	/csss
	   layout.css

SQL FILES:
    create_tables.sql
    insert_data.sql
    queries.sql

MAIN FILE:
    app.py

========================================================
4. DATABASE DESIGN
========================================================

Main tables:

- STUDENTS
- INSTRUCTOR
- COURSE
- ENROLLMENT
- GRADE
- USERS
- DEPARTMENT
- PHONES
- LOGS

Relationships:

- Students ↔ Courses (Many-to-Many via ENROLLMENT)
- Courses ↔ Instructor (One-to-Many)
- Students ↔ Grades (One-to-Many via ENROLLMENT)
- Users linked to Students or Instructors

========================================================
5. MAIN FEATURES IMPLEMENTED
========================================================

Role-based login system
Student CRUD (Create, Read, Update, Delete)
Course management
Enrollment system
Grade management system
GPA calculation system
Student transcript generation
Grade distribution statistics
Dashboard with role-based statistics
Secure API using role validation headers

========================================================
6. ADVANCED SQL FEATURES
========================================================

Views (Student Transcript View)
Stored Procedures (Grade insertion)
Triggers (Automatic GPA calculation)
Transactions (Enrollment rollback with logs)
Aggregation queries (GROUP BY, HAVING)
Complex JOIN queries

========================================================
7. SECURITY IMPLEMENTATION
========================================================

- Role-based access control
- Basic authentication via localStorage session
- Backend validation using Flask decorators
- Parameterized SQL queries to prevent SQL injection

========================================================
8. HOW TO RUN THE PROJECT
========================================================

1. Install dependencies:
   pip install flask flask-cors pyodbc

2. Start SQL Server and create database:
   Execute:
   - create_tables.sql
   - insert_data.sql
   - queries.sql

3. Run backend server:
   python app.py

4. Open frontend:
   Open dashboard.html or login.html in browser

========================================================
9. KNOWN LIMITATIONS
========================================================

- Some reports depend on view definitions
- GPA calculation depends on grade trigger setup
- Requires SQL Server ODBC Driver 17
- Local development environment only

========================================================
10. AUTHOR DECLARATION
========================================================

This project was developed as an academic assignment.

If any AI tools  were used, 
they were used only for assistance in debugging and learning purposes,
also to present a Project with an profesional aspect,
not for full automatic generation of the project.

All core logic, database design, and implementation decisions 
were made by the student, only corrected by the AI if necessary.

