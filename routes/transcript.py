from flask import Blueprint, jsonify
from db import get_connection
from utils.auth import require_role

transcript_bp = Blueprint("transcript", __name__)

@transcript_bp.route("/transcript/<student_id>", methods=["GET"])
@require_role(["admin", "teacher", "student"])
def get_transcript(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        ID_STUDENT,
        NAME_STUDENT,
        NAME_COURSE,
        CREDITS,
        FINAL_GRADE,
        GPA
    FROM VW_STUDENT_TRANSCRIPT
    WHERE ID_STUDENT = ?
    """

    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()

    transcript = []
    total_credits = 0
    total_gpa = 0

    for row in rows:

        transcript.append({
            "id_student": row[0],
            "name_student": row[1],
            "course": row[2],
            "credits": row[3],
            "final_grade": row[4],
            "gpa_points": row[5]
        })

        total_credits += row[3]
        total_gpa += row[5]

    avg_gpa = round(total_gpa / len(rows), 2) if rows else 0

    conn.close()

    return jsonify({
        "student": student_id,
        "total_credits": total_credits,
        "avg_gpa": avg_gpa,
        "transcript": transcript
    })