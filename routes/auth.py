from flask import Blueprint, request
from db import get_connection

auth_bp = Blueprint("auth", __name__)

# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        ID_USER,
        USERNAME,
        ROLE_USER,
        ID_STUDENT,
        ID_INSTRUCTOR
    FROM USERS
    WHERE USERNAME = ?
    AND PASSWORD_USER = ?
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        return {
            "success": True,
            "user": {
                "id_user": user[0],
                "username": user[1],
                "role": user[2],
                "id_student": user[3],
                "id_instructor": user[4]
            }
        }

    return {
        "success": False,
        "message": "Invalid credentials"
    }, 401