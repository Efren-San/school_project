from flask import request

def require_role(allowed_roles):

    role = request.headers.get("Role")

    if role not in allowed_roles:

        return {
            "error": "Unauthorized"
        }, 403

    return None