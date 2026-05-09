from flask import Blueprint
from db import get_connection

stats_bp = Blueprint("stats", __name__)

# =========================
# DASHBOARD STATS
# =========================

@stats_bp.route("/stats", methods=["GET"])
def get_stats():

    conn = get_connection()

    cursor = conn.cursor()

    # STUDENTS
    cursor.execute(
        "SELECT COUNT(*) FROM STUDENTS"
    )

    total_students = cursor.fetchone()[0]

    # COURSES
    cursor.execute(
        "SELECT COUNT(*) FROM COURSE"
    )

    total_courses = cursor.fetchone()[0]

    # ENROLLMENTS
    cursor.execute(
        "SELECT COUNT(*) FROM ENROLLMENT"
    )

    total_enrollments = cursor.fetchone()[0]

    # AVG GPA
    cursor.execute(
        "SELECT AVG(GPA) FROM GRADE"
    )

    avg_gpa = cursor.fetchone()[0]

    conn.close()

    return {
        "students": total_students,
        "courses": total_courses,
        "enrollments": total_enrollments,
        "avg_gpa": round(avg_gpa, 2)
            if avg_gpa
            else 0
    }