from flask import Blueprint, request, jsonify
from db import get_connection

@dashboard_bp.route("/dashboard", methods=["GET"])
@require_role(["admin", "teacher", "student"])
def get_dashboard():


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard():

    role = request.headers.get("Role")
    user_id_student = request.headers.get("Student-Id")

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # ADMIN DASHBOARD
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

        conn.close()

        return jsonify({
            "role": "admin",
            "stats": {
                "students": students,
                "courses": courses,
                "enrollments": enrollments,
                "avg_gpa": round(avg_gpa, 2)
            },
            "actions": [
                "manage_students",
                "manage_courses",
                "manage_enrollments"
            ]
        })


    # =========================
    # TEACHER DASHBOARD
    # =========================
    if role == "teacher":

        cursor.execute("""
            SELECT COUNT(*)
            FROM COURSE
            WHERE ID_INSTRUCTOR = (
                SELECT ID_INSTRUCTOR FROM USERS WHERE ROLE_USER='teacher'
            )
        """)
        courses = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM ENROLLMENT
        """)
        enrollments = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            "role": "teacher",
            "stats": {
                "courses": courses,
                "enrollments": enrollments
            },
            "actions": [
                "my_courses",
                "grades",
                "enrollments"
            ]
        })


    # =========================
    # STUDENT DASHBOARD
    # =========================
    if role == "student":

        cursor.execute("""
            SELECT COUNT(*)
            FROM ENROLLMENT
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

        conn.close()

        return jsonify({
            "role": "student",
            "stats": {
                "courses": courses,
                "avg_gpa": round(avg_gpa, 2)
            },
            "actions": [
                "my_courses",
                "my_grades"
            ]
        })


    return jsonify({"error": "Invalid role"}), 403