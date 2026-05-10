from flask import Blueprint, request, jsonify
from db import get_connection
from utils.auth import require_role

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
@require_role(["admin", "teacher", "student"])
def get_dashboard():

    role = request.headers.get("Role")
    user_id_student = request.headers.get("Student-Id")
    user_id_instructor = request.headers.get("Instructor-Id")

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # =========================
    # ADMIN
    # =========================
    if role == "admin":

        cursor.execute("SELECT COUNT(*) FROM STUDENTS")
        students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM COURSE")
        courses = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ENROLLMENT")
        enrollments = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(GPA) FROM GRADE")
        avg_gpa = cursor.fetchone()[0] or 0

        stats = {
            "card1_title": "Students",
            "card1_value": students,
            "card2_title": "Courses",
            "card2_value": courses,
            "card3_title": "Enrollments",
            "card3_value": enrollments,
            "card4_title": "Avg GPA",
            "card4_value": round(avg_gpa, 2)
        }

    # =========================
    # TEACHER
    # =========================
    elif role == "teacher":

        cursor.execute("""
            SELECT COUNT(*) FROM COURSE
            WHERE ID_INSTRUCTOR = ?
        """, (user_id_instructor,))
        courses = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM ENROLLMENT E
            INNER JOIN COURSE C ON E.ID_COURSE = C.ID_COURSE
            WHERE C.ID_INSTRUCTOR = ?
        """, (user_id_instructor,))
        students = cursor.fetchone()[0]

        stats = {
            "card1_title": "My Courses",
            "card1_value": courses,
            "card2_title": "My Students",
            "card2_value": students,
            "card3_title": "Pending Grades",
            "card3_value": 0,
            "card4_title": "Class Avg GPA",
            "card4_value": 0
        }

    # =========================
    # STUDENT
    # =========================
    elif role == "student":

        cursor.execute("""
            SELECT COUNT(*) FROM ENROLLMENT
            WHERE ID_STUDENT = ?
        """, (user_id_student,))
        courses = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(GPA)
            FROM GRADE G
            INNER JOIN ENROLLMENT E
            ON G.ID_ENROLLMENT = E.ID_ENROLLMENT
            WHERE E.ID_STUDENT = ?
        """, (user_id_student,))
        avg_gpa = cursor.fetchone()[0] or 0

        stats = {
            "card1_title": "My Courses",
            "card1_value": courses,
            "card2_title": "My GPA",
            "card2_value": round(avg_gpa, 2),
            "card3_title": "Passed",
            "card3_value": 0,
            "card4_title": "Semester",
            "card4_value": "-"
        }

    conn.close()

    return jsonify({
        "role": role,
        "stats": stats,
        "actions": []
    })