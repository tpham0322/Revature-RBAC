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
