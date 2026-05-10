from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    # Validación básica
    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password required"
        }), 400

    try:
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

            return jsonify({
                "success": True,
                "user": {
                    "id_user": user[0],
                    "username": user[1],
                    "role": user[2],
                    "id_student": user[3],
                    "id_instructor": user[4]
                }
            }), 200


        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Server error",
            "error": str(e)
        }), 500