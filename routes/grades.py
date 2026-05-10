from flask import Blueprint, jsonify
from db import get_connection
from utils.auth import require_role

grades_bp = Blueprint("grades", __name__)

# =========================
# GET ALL GRADES
# =========================

@grades_bp.route("/grades", methods=["GET"])
@require_role(["admin", "teacher", "student"])
def get_grades():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        G.ID_GRADE,
        S.NAME_STUDENT,
        C.NAME_COURSE,
        G.FINAL_GRADE,
        G.GPA
    FROM GRADE G
    INNER JOIN ENROLLMENT E
        ON G.ID_ENROLLMENT = E.ID_ENROLLMENT
    INNER JOIN STUDENTS S
        ON E.ID_STUDENT = S.ID_STUDENT
    INNER JOIN COURSE C
        ON E.ID_COURSE = C.ID_COURSE
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    grades = []

    for row in rows:

        grades.append({
            "id_grade": row[0],
            "student": row[1],
            "course": row[2],
            "final_grade": float(row[3]),
            "gpa": float(row[4]) if row[4] is not None else 0
        })

    conn.close()

    return jsonify(grades)

# =========================
# GET ONE GRADE
# =========================

@grades_bp.route("/grades/<id>", methods=["GET"])
def get_grade(id):

    auth = require_role(["admin", "teacher", "student"])

    if auth:
        return auth

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        G.ID_GRADE,
        S.NAME_STUDENT,
        C.NAME_COURSE,
        G.FINAL_GRADE,
        G.GPA
    FROM GRADE G

    INNER JOIN ENROLLMENT E
    ON G.ID_ENROLLMENT = E.ID_ENROLLMENT

    INNER JOIN STUDENTS S
    ON E.ID_STUDENT = S.ID_STUDENT

    INNER JOIN COURSE C
    ON E.ID_COURSE = C.ID_COURSE

    WHERE G.ID_GRADE = ?
    """

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "error": "Grade not found"
        }, 404

    grade = {
        "id_grade": row[0],
        "student": row[1],
        "course": row[2],
        "final_grade": float(row[3]),
        "gpa": float(row[4]) if row[4] is not None else 0
    }

    return grade


# =========================
# CREATE GRADE
# =========================

@grades_bp.route("/grades", methods=["POST"])
def create_grade():

    # admin y teacher pueden ingresar notas
    auth = require_role(["admin", "teacher"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO GRADE(
            ID_ENROLLMENT,
            FINAL_GRADE
        )
        VALUES (?, ?)
        """

        cursor.execute(
            query,
            (
                data.get("id_enrollment"),
                data.get("final_grade")
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Grade created successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# UPDATE GRADE
# =========================

@grades_bp.route("/grades/<id>", methods=["PUT"])
def update_grade(id):

    # admin y teacher pueden modificar notas
    auth = require_role(["admin", "teacher"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        UPDATE GRADE
        SET
            FINAL_GRADE = ?
        WHERE ID_GRADE = ?
        """

        cursor.execute(
            query,
            (
                data.get("final_grade"),
                id
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Grade updated successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500


# =========================
# DELETE GRADE
# =========================

@grades_bp.route("/grades/<id>", methods=["DELETE"])
def delete_grade(id):

    # SOLO admin puede eliminar notas
    auth = require_role(["admin"])

    if auth:
        return auth

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        DELETE FROM GRADE
        WHERE ID_GRADE = ?
        """

        cursor.execute(query, (id,))

        conn.commit()

        conn.close()

        return {
            "message": "Grade deleted successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }, 500