from flask import Blueprint, jsonify
from db import get_connection
from utils.auth import require_role

students_bp = Blueprint("students", __name__)

# =========================
# GET STUDENTS
# =========================

@students_bp.route("/students", methods=["GET"])
@require_role(["admin", "teacher"])
def get_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ID_STUDENT,
            NAME_STUDENT,
            BIRTHDATE,
            GENDER,
            ENROLLMENT_YEAR,
            ID_DEPARTMENT
        FROM STUDENTS
    """)

    rows = cursor.fetchall()

    students = []

    for row in rows:

        students.append({
            "id_student": row[0],
            "name_student": row[1],
            "birthdate": str(row[2]),
            "gender": row[3],
            "enrollment_year": row[4],
            "id_department": row[5]
        })

    conn.close()

    return jsonify(students)


# =========================
# GET ONE STUDENT
# =========================

@students_bp.route("/students/<id>", methods=["GET"])
def get_student(id):

    # admin, teacher y student pueden entrar
    auth = require_role(["admin", "teacher", "student"])

    if auth:
        return auth

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM STUDENTS
    WHERE ID_STUDENT = ?
    """

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "error": "Student not found"
        }, 404

    student = {
        "id_student": row[0],
        "name_student": row[1],
        "birthdate": str(row[2]),
        "gender": row[3],
        "enrollment_year": row[4],
        "id_department": row[5]
    }

    return student


# =========================
# POST STUDENT
# =========================

@students_bp.route("/students", methods=["POST"])
def create_student():

    # SOLO admin puede crear
    auth = require_role(["admin"])

    if auth:
        return auth

    try:

        data = request.json

        if not data:

            return {
                "error": "No JSON received"
            }, 400

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO STUDENTS(
            ID_STUDENT,
            NAME_STUDENT,
            BIRTHDATE,
            GENDER,
            ENROLLMENT_YEAR,
            ID_DEPARTMENT
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                data.get("id_student"),
                data.get("name_student"),
                data.get("birthdate"),
                data.get("gender"),
                data.get("enrollment_year"),
                data.get("id_department")
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Student created successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# UPDATE STUDENT
# =========================

@students_bp.route("/students/<id>", methods=["PUT"])
def update_student(id):

    # SOLO admin puede editar
    auth = require_role(["admin"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        UPDATE STUDENTS
        SET
            NAME_STUDENT = ?,
            BIRTHDATE = ?,
            GENDER = ?,
            ENROLLMENT_YEAR = ?,
            ID_DEPARTMENT = ?
        WHERE ID_STUDENT = ?
        """

        cursor.execute(
            query,
            (
                data.get("name_student"),
                data.get("birthdate"),
                data.get("gender"),
                data.get("enrollment_year"),
                data.get("id_department"),
                id
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Student updated successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# DELETE STUDENT
# =========================

@students_bp.route("/students/<id>", methods=["DELETE"])
def delete_student(id):

    # SOLO admin puede eliminar
    auth = require_role(["admin"])

    if auth:
        return auth

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        DELETE FROM STUDENTS
        WHERE ID_STUDENT = ?
        """

        cursor.execute(query, (id,))

        conn.commit()

        conn.close()

        return {
            "message": "Student deleted successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500