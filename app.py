
from flask import Flask, jsonify, abort, request, g
import db_creation.db as db
from auth_check import enforce_rbac, can_access

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
    order = db.get_order(order_id)
    # Returns 404 for both so attacker won't know whether resource exists or not
    if not order or not can_access(g.user, order):
        abort(404, description="Order does not exist")

    return jsonify(order)


@app.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("item", "amount")):
        abort(400, description="Missing required fields")

    order_id = db.create_order(
        owner_id = g.user.get("id"), # Instead of taking owner_id from the request, get the current authenticated user id
        item = data["item"],
        amount = data["amount"]
    )

    return jsonify(message="Order created", id=order_id), 201


@app.put("/orders/<int:order_id>")
def update_order(order_id):
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("item", "amount")):
        abort(400, description="Missing required fields")
 
    order = db.get_order(order_id)
    if not order or not can_access(g.user, order): # Is the current authenticated user allowed to update the order
        abort(404, description="Order not found")

    db.update_order(order_id, data["item"], data["amount"])

    return jsonify(message="Order updated")


@app.delete("/orders/<int:order_id>")
def delete_order(order_id):
    order = db.get_order(order_id)
    if not order or not can_access(g.user, order):
        abort(404, description="Order not found")

    db.delete_order(order_id)
    return jsonify(message="Order deleted")


# -------------------------
# DOCUMENTS
# -------------------------

@app.get("/documents/<int:doc_id>")
def get_document(doc_id):

    doc = db.get_document(doc_id)

    if not doc or not can_access(g.user, doc):
        abort(404, "Document does not exist")

    return jsonify(doc)


@app.post("/documents")
def create_document():
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ( "title", "content")):
        return jsonify(error="Missing required fields"), 400

    doc_id = db.create_document(
        owner_id = g.user.get("id"),
        title = data["title"],
        content = data["content"]
    )

    return jsonify(message="Document created", id=doc_id), 201


@app.put("/documents/<int:doc_id>")
def update_document(doc_id):
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("title", "content")):
        abort(400, description="Missing required fields")

    doc = db.get_document(doc_id)
    if not doc or not can_access(g.user, doc):
        abort(404, description="Document not found")

    db.update_document(
        doc_id,
        data["title"],
        data["content"]
    )

    return jsonify(message="Document updated")


@app.delete("/documents/<int:doc_id>")
def delete_document(doc_id):
    doc = db.get_document(doc_id)
    if not doc or not can_access(g.user, doc):
        abort(404, description="Document not found")

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
