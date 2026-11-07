
from flask import Flask, jsonify, abort, request
import db_creation.db as db

app = Flask(__name__)


# -------------------------
# Error Handler
# -------------------------
@app.errorhandler(401)
def handle_unauthorized(error):
    response = jsonify({
        "error": "Unauthorized",
        "message": error.message
    })
    return response, 401

@app.errorhandler(403)
def handle_unauthorized(error):
    response = jsonify({
        "error": "Forbidden",
        "message": error.message
    })
    return response, 403

@app.errorhandler(404)
def handle_unauthorized(error):
    response = jsonify({
        "error": "Not found",
        "message": error.message
    })
    return response, 404


@app.route("/test")
def test():
    return jsonify(status="ok")


# -------------------------
# ORDERS
# -------------------------

@app.get("/orders")
def list_orders():
    return jsonify(db.get_all_orders())


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    """Vulnerable: allows any user to access any order"""
    order = db.get_order(order_id)

    if not order:
        abort(404)

    return jsonify(order)


@app.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("owner_id", "item", "amount")):
        return jsonify(error="Missing required fields"), 400

    order_id = db.create_order(
        data["owner_id"],
        data["item"],
        data["amount"]
    )

    return jsonify(message="Order created", id=order_id), 201


@app.put("/orders/<int:order_id>")
def update_order(order_id):
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("item", "amount")):
        return jsonify(error="Missing required fields"), 400

    if not db.get_order(order_id):
        return jsonify(error="Order not found"), 404

    db.update_order(order_id, data["item"], data["amount"])

    return jsonify(message="Order updated")


@app.delete("/orders/<int:order_id>")
def delete_order(order_id):
    if not db.delete_order(order_id):
        return jsonify(error="Order not found"), 404

    return jsonify(message="Order deleted")


# -------------------------
# DOCUMENTS
# -------------------------

@app.get("/documents")
def list_documents():
    return jsonify(db.get_all_documents())


@app.get("/documents/<int:doc_id>")
def get_document(doc_id):
    """Vulnerable: allows any user to access any document"""
    doc = db.get_document(doc_id)

    if not doc:
        abort(404)

    return jsonify(doc)


@app.post("/documents")
def create_document():
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("owner_id", "title", "content")):
        return jsonify(error="Missing required fields"), 400

    doc_id = db.create_document(
        data["owner_id"],
        data["title"],
        data["content"]
    )

    return jsonify(message="Document created", id=doc_id), 201


@app.put("/documents/<int:doc_id>")
def update_document(doc_id):
    data = request.get_json(silent=True) or {}

    if not all(k in data for k in ("title", "content")):
        return jsonify(error="Missing required fields"), 400

    if not db.get_document(doc_id):
        return jsonify(error="Document not found"), 404

    db.update_document(
        doc_id,
        data["title"],
        data["content"]
    )

    return jsonify(message="Document updated")


@app.delete("/documents/<int:doc_id>")
def delete_document(doc_id):
    if not db.delete_document(doc_id):
        return jsonify(error="Document not found"), 404

    return jsonify(message="Document deleted")


# -------------------------
# ADMIN
# -------------------------

@app.get("/admin/users")
def list_users():
    """Vulnerable: allows any user to access admin endpoint"""
    return jsonify(db.get_all_users())


if __name__ == "__main__":
    app.run(debug=True)
