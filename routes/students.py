from flask import Blueprint, request
from db import get_connection

students_bp = Blueprint("students", __name__)

# =========================
# GET STUDENTS
# =========================

@students_bp.route("/students", methods=["GET"])
def get_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM STUDENTS")

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

    return students


# =========================
# POST STUDENT
# =========================

@students_bp.route("/students", methods=["POST"])
def create_student():

    try:

        data = request.json

        # Validar si llega JSON
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