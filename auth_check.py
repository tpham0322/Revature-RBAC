from flask import abort, g, request
import db_creation.db as db

# -------------------------
# RBAC Implementation
# -------------------------

ROLES = [
    {"role": "user", 
     "permissions": [
        "get_order", "create_order", "update_order", "delete_order",
        "get_document", "create_document", "update_document", "delete_document",
        ]
    },
    {"role": "admin", 
     "permissions": [
        "list_users", "delete_user",
        ]
    },
]

ROLE_PERMISSIONS = {r["role"]: r["permissions"] for r in ROLES}

# -------------------------
# Authentication
# -------------------------

def get_current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, message="Login required")

    current_user = db.get_user(auth.removeprefix("Bearer "))
    if not current_user:
        abort(401, message="User does not exist")

    return current_user