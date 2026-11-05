from flask import Flask, jsonify, abort
import db_creation.db as db

app = Flask(__name__)

@app.route("/test")
def test():
    return jsonify(status="ok")

@app.get("/orders/<int:order_id>")
def get_order(order_id):
    """Vulnerable: allows any user to access any order"""
    order = db.get_order(order_id)
    if not order:
        abort(404)
    return jsonify(order)

@app.get("/documents/<int:doc_id>")
def get_document(doc_id):
    """Vulnerable: allows any user to access any document"""
    doc = db.get_document(doc_id)
    if not doc:
        abort(404)
    return jsonify(doc)

@app.get("/admin/users")
def list_users():
    """Vulnerable: allows any user to access admin endpoint"""
    return jsonify(db.get_all_users())

if __name__ == "__main__":
    app.run(debug=True)
