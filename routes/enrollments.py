from flask import Blueprint, request
from db import get_connection
from utils.auth import require_role

enrollments_bp = Blueprint("enrollments", __name__)

# =========================
# GET ALL ENROLLMENTS
# =========================

@enrollments_bp.route("/enrollments", methods=["GET"])
def get_enrollments():

    # admin y teacher pueden ver enrollments
    auth = require_role(["admin", "teacher"])

    if auth:
        return auth

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        E.ID_ENROLLMENT,
        S.NAME_STUDENT,
        C.NAME_COURSE,
        E.ENROLLMENT_DATE,
        E.SEMESTER
    FROM ENROLLMENT E

    INNER JOIN STUDENTS S
    ON E.ID_STUDENT = S.ID_STUDENT

    INNER JOIN COURSE C
    ON E.ID_COURSE = C.ID_COURSE
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    enrollments = []

    for row in rows:

        enrollments.append({
            "id_enrollment": row[0],
            "student": row[1],
            "course": row[2],
            "enrollment_date": str(row[3]),
            "semester": row[4]
        })

    conn.close()

    return enrollments


# =========================
# GET ONE ENROLLMENT
# =========================

@enrollments_bp.route("/enrollments/<id>", methods=["GET"])
def get_enrollment(id):

    auth = require_role(["admin", "teacher", "student"])

    if auth:
        return auth

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        E.ID_ENROLLMENT,
        S.NAME_STUDENT,
        C.NAME_COURSE,
        E.ENROLLMENT_DATE,
        E.SEMESTER
    FROM ENROLLMENT E

    INNER JOIN STUDENTS S
    ON E.ID_STUDENT = S.ID_STUDENT

    INNER JOIN COURSE C
    ON E.ID_COURSE = C.ID_COURSE

    WHERE E.ID_ENROLLMENT = ?
    """

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "error": "Enrollment not found"
        }, 404

    enrollment = {
        "id_enrollment": row[0],
        "student": row[1],
        "course": row[2],
        "enrollment_date": str(row[3]),
        "semester": row[4]
    }

    return enrollment


# =========================
# CREATE ENROLLMENT
# =========================

@enrollments_bp.route("/enrollments", methods=["POST"])
def create_enrollment():

    # admin y student pueden inscribirse
    auth = require_role(["admin", "student"])

    if auth:
        return auth

    try:

        data = request.json

        conn = get_connection()

        cursor = conn.cursor()

        # =========================
        # VALIDAR STUDENT
        # =========================

        check_student = """
        SELECT *
        FROM STUDENTS
        WHERE ID_STUDENT = ?
        """

        cursor.execute(
            check_student,
            (data.get("id_student"),)
        )

        student = cursor.fetchone()

        if not student:

            conn.close()

            return {
                "error": "Student not found"
            }, 404

        # =========================
        # VALIDAR COURSE
        # =========================

        check_course = """
        SELECT CAPACITY
        FROM COURSE
        WHERE ID_COURSE = ?
        """

        cursor.execute(
            check_course,
            (data.get("id_course"),)
        )

        course = cursor.fetchone()

        if not course:

            conn.close()

            return {
                "error": "Course not found"
            }, 404

        capacity = course[0]

        # =========================
        # VALIDAR DUPLICADO
        # =========================

        check_duplicate = """
        SELECT *
        FROM ENROLLMENT
        WHERE ID_STUDENT = ?
        AND ID_COURSE = ?
        AND SEMESTER = ?
        """

        cursor.execute(
            check_duplicate,
            (
                data.get("id_student"),
                data.get("id_course"),
                data.get("semester")
            )
        )

        duplicate = cursor.fetchone()

        if duplicate:

            conn.close()

            return {
                "error": "Student already enrolled"
            }, 400

        # =========================
        # VALIDAR CAPACIDAD
        # =========================

        count_query = """
        SELECT COUNT(*)
        FROM ENROLLMENT
        WHERE ID_COURSE = ?
        AND SEMESTER = ?
        """

        cursor.execute(
            count_query,
            (
                data.get("id_course"),
                data.get("semester")
            )
        )

        current_students = cursor.fetchone()[0]

        if current_students >= capacity:

            conn.close()

            return {
                "error": "Course is full"
            }, 400

        # =========================
        # INSERT ENROLLMENT
        # =========================

        query = """
        INSERT INTO ENROLLMENT(
            ID_STUDENT,
            ID_COURSE,
            ENROLLMENT_DATE,
            SEMESTER
        )
        VALUES (?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                data.get("id_student"),
                data.get("id_course"),
                data.get("enrollment_date"),
                data.get("semester")
            )
        )

        conn.commit()

        conn.close()

        return {
            "message": "Enrollment created successfully"
        }

    except Exception as e:

        conn.rollback()

        conn.close()

        return {
            "error": str(e)
        }, 500


# =========================
# DELETE ENROLLMENT
# =========================

@enrollments_bp.route("/enrollments/<id>", methods=["DELETE"])
def delete_enrollment(id):

    # admin y student pueden darse de baja
    auth = require_role(["admin", "student"])

    if auth:
        return auth

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # =========================
        # VALIDAR ENROLLMENT
        # =========================

        check_query = """
        SELECT *
        FROM ENROLLMENT
        WHERE ID_ENROLLMENT = ?
        """

        cursor.execute(check_query, (id,))

        enrollment = cursor.fetchone()

        if not enrollment:

            conn.close()

            return {
                "error": "Enrollment not found"
            }, 404

        # =========================
        # INSERT LOG
        # =========================

        log_query = """
        INSERT INTO LOGS(
            ACTION_TYPE,
            DESCRIPTION_LOG,
            ACTION_DATE
        )
        VALUES (
            'DROP COURSE',
            ?,
            GETDATE()
        )
        """

        description = f"Enrollment {id} deleted"

        cursor.execute(log_query, (description,))

        # =========================
        # DELETE ENROLLMENT
        # =========================

        delete_query = """
        DELETE FROM ENROLLMENT
        WHERE ID_ENROLLMENT = ?
        """

        cursor.execute(delete_query, (id,))

        conn.commit()

        conn.close()

        return {
            "message": "Enrollment deleted successfully"
        }

    except Exception as e:

        conn.rollback()

        conn.close()

        return {
            "error": str(e)
        }, 500