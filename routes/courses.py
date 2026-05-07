from flask import Blueprint
from db import get_connection

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/courses", methods=["GET"])
def get_courses():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM COURSE")

    rows = cursor.fetchall()

    courses = []

    for row in rows:

        courses.append({
            "id_course": row[0],
            "name_course": row[1],
            "credits": row[2],
            "id_instructor": row[3],
            "id_department": row[4],
            "semester": row[5],
            "capacity": row[6]
        })

    conn.close()

    return courses