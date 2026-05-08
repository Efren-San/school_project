from flask import request

def require_role(allowed_roles):

    role = request.headers.get("Role")

    # No mandó rol
    if not role:

        return {
            "error": "Unauthorized"
        }, 401

    # Rol sin permisos
    if role not in allowed_roles:

        return {
            "error": "Access denied"
        }, 403

    return None