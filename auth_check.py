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


# ----------------------------------------
# Function Level Authorization (BFLA fix)
# ----------------------------------------

def has_permission(user, permission):
    return permission in ROLE_PERMISSIONS.get(user["role"], [])

def enforce_rbac():
    """
    Will run before every request to:
    1. Get the current user and set it for the current session (via Flask.g)
    2. Check authorization for the request based on the users role/permissions
    """
    g.user = get_current_user()
    if not has_permission(g.user, request.endpoint):
        abort(403)

# ----------------------------------------
# Object Level Authorization (BOLA fix)
# ----------------------------------------

def can_access(current_user, resource):
    """Authorization check, can current user access the requested document/order"""
    return resource.get("owner_id") == current_user.get("id")

def load_resource(db_function, resource_id):
    resource = db_function(resource_id)
    if not resource or not can_access(g.user, resource):
        abort(404)
    return resource