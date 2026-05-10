from flask import Blueprint, request, jsonify
from db import get_connection
from utils.auth import require_role

courses_bp = Blueprint("courses", __name__)

# =========================
# GET COURSES
# =========================

@courses_bp.route("/courses", methods=["GET"])
@require_role(["admin", "teacher", "student"])
def get_courses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ID_COURSE,
            NAME_COURSE,
            CREDITS,
            SEMESTER
        FROM COURSE
    """)

    rows = cursor.fetchall()

    conn.close()

    courses = []

    for row in rows:

        courses.append({
            "id_course": row[0],
            "name_course": row[1],
            "credits": row[2],
            "semester": row[3]
        })

    return jsonify(courses)

# =========================
# GET ONE COURSE
# =========================

@courses_bp.route("/courses/<id>", methods=["GET"])
def get_course(id):

    auth = require_role(["admin", "teacher", "student"])

    if auth:
        return auth

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM COURSE
    WHERE ID_COURSE = ?
    """

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "error": "Course not found"
        }, 404

    course = {
        "id_course": row[0],
        "name_course": row[1],
        "credits": row[2],
        "id_instructor": row[3],
        "id_department": row[4],
        "semester": row[5],
        "capacity": row[6]
    }

    return course


# =========================
# CREATE COURSE
# =========================

@courses_bp.route("/courses", methods=["POST"])
def create_course():

    # admin y teacher pueden crear cursos
    auth = require_role(["admin", "teacher"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO COURSE(
            ID_COURSE,
            NAME_COURSE,
            CREDITS,
            ID_INSTRUCTOR,
            ID_DEPARTMENT,
            SEMESTER,
            CAPACITY
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                data.get("id_course"),
                data.get("name_course"),
                data.get("credits"),
                data.get("id_instructor"),
                data.get("id_department"),
                data.get("semester"),
                data.get("capacity")
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Course created successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# UPDATE COURSE
# =========================

@courses_bp.route("/courses/<id>", methods=["PUT"])
def update_course(id):

    # admin y teacher pueden editar cursos
    auth = require_role(["admin", "teacher"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        UPDATE COURSE
        SET
            NAME_COURSE = ?,
            CREDITS = ?,
            ID_INSTRUCTOR = ?,
            ID_DEPARTMENT = ?,
            SEMESTER = ?,
            CAPACITY = ?
        WHERE ID_COURSE = ?
        """

        cursor.execute(
            query,
            (
                data.get("name_course"),
                data.get("credits"),
                data.get("id_instructor"),
                data.get("id_department"),
                data.get("semester"),
                data.get("capacity"),
                id
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Course updated successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# DELETE COURSE
# =========================

@courses_bp.route("/courses/<id>", methods=["DELETE"])
def delete_course(id):

    # SOLO admin puede eliminar cursos
    auth = require_role(["admin"])

    if auth:
        return auth

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        DELETE FROM COURSE
        WHERE ID_COURSE = ?
        """

        cursor.execute(query, (id,))

        conn.commit()

        conn.close()

        return {
            "message": "Course deleted successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500