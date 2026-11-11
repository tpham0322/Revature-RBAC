
from flask import Flask, jsonify, abort, request, g
import db_creation.db as db
from auth_check import enforce_rbac, owner_check

app = Flask(__name__)
app.before_request(enforce_rbac)    

# -------------------------
# Error Handler
# -------------------------

@app.errorhandler(400)
def handle_bad_request(error):
    response = jsonify({
        "error": "Bad Request",
        "message": error.description
    })
    return response, 400

@app.errorhandler(401)
def handle_unauthorized(error):
    response = jsonify({
        "error": "Unauthorized",
        "message": error.description
    })
    return response, 401

@app.errorhandler(403)
def handle_forbidden(error):
    response = jsonify({
        "error": "Forbidden",
        "message": error.description
    })
    return response, 403

@app.errorhandler(404)
def handle_not_found(error):
    response = jsonify({
        "error": "Resource Not found",
        "message": error.description
    })
    return response, 404

def field_check(*fields):
    data = request.get_json(silent=True) or {}
    if not all(f in data for f in fields):
        abort(400, description="Missing required fields")
    return data
    

# -------------------------
# HEALTH CHECK
# -------------------------

@app.route("/test")
def test():
    return jsonify(status="ok")


# -------------------------
# ORDERS
# -------------------------

@app.get("/orders/<int:order_id>")
def get_order(order_id):
    return jsonify(owner_check(db.get_order, order_id))


@app.post("/orders")
def create_order():
    data = field_check("item", "amount")
    order_id = db.create_order(
        owner_id = g.user.get("id"), # Instead of taking owner_id from the request, get the current authenticated user id
        item = data["item"],
        amount = data["amount"]
    )
    return jsonify(message="Order created", id=order_id), 201


@app.put("/orders/<int:order_id>")
def update_order(order_id):
    data = field_check("item", "amount")
    owner_check(db.get_order, order_id)
    db.update_order(order_id, data["item"], data["amount"])
    return jsonify(message="Order updated")


@app.delete("/orders/<int:order_id>")
def delete_order(order_id):
    owner_check(db.get_order, order_id)
    db.delete_order(order_id)
    return jsonify(message="Order deleted")


# -------------------------
# DOCUMENTS
# -------------------------

@app.get("/documents/<int:doc_id>")
def get_document(doc_id):
    return jsonify(owner_check(db.get_document, doc_id))

@app.post("/documents")
def create_document():
    data = field_check("title", "content")
    doc_id = db.create_document(
        owner_id = g.user.get("id"),
        title = data["title"],
        content = data["content"]
    )
    return jsonify(message="Document created", id=doc_id), 201


@app.put("/documents/<int:doc_id>")
def update_document(doc_id):
    data = field_check("title", "content")
    owner_check(db.get_document, doc_id)
    db.update_document(
        doc_id,
        data["title"],
        data["content"]
    )
    return jsonify(message="Document updated")


@app.delete("/documents/<int:doc_id>")
def delete_document(doc_id):
    owner_check(db.get_document, doc_id)
    db.delete_document(doc_id)
    return jsonify(message="Document deleted")


# -------------------------
# ADMIN
# -------------------------

@app.get("/admin/users")
def list_users():
    return jsonify(db.get_all_users())

if __name__ == "__main__":
    app.run(debug=True)
