from functools import wraps
from flask import request, jsonify

def require_role(allowed_roles):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            role = request.headers.get("Role")

            if not role:
                return jsonify({"error": "Unauthorized"}), 401

            if role not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator  