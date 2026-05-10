from functools import wraps
from flask import request, jsonify

def require_role(allowed_roles):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            role = request.headers.get("Role")

            student_id = request.headers.get("Student-Id")
            instructor_id = request.headers.get("Instructor-Id")

            if not role:
                return jsonify({"error": "Unauthorized"}), 401

            if role not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403

            # opcional debug
            request.user_role = role
            request.student_id = student_id
            request.instructor_id = instructor_id

            return f(*args, **kwargs)

        return wrapper

    return decorator