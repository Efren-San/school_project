from flask import Blueprint, jsonify
from db import get_connection
from utils.auth import require_role

department_bp = Blueprint("department", __name__)

@department_bp.route("/departments/ranking", methods=["GET"])
@require_role(["admin", "teacher"])
def department_ranking():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        ID_DEPARTMENT,
        NAME_DEPARTMENT,
        TOTAL_STUDENTS,
        AVG_GPA
    FROM VW_DEPARTMENT_RANKING
    ORDER BY AVG_GPA DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "id_department": row[0],
            "name_department": row[1],
            "total_students": row[2],
            "avg_gpa": float(row[3]) if row[3] else 0
        })

    conn.close()

    return jsonify(result)