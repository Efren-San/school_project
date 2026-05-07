from flask import Blueprint
from db import get_connection

grades_bp = Blueprint("grades", __name__)

@grades_bp.route("/grades", methods=["GET"])
def get_grades():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
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
            "student": row[0],
            "course": row[1],
            "final_grade": float(row[2]),
            "gpa": float(row[3]) if row[3] is not None else 0
        })

    conn.close()

    return grades