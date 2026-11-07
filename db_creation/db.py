import sqlite3
from pathlib import Path

# in case populate.py is run from a different directory
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR/"rev-rbac.db"

def create_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_db():
    conn = create_conn()
    conn.executescript((BASE_DIR / "schema.sql").read_text())
    conn.executescript((BASE_DIR / "sample_data.sql").read_text())
    conn.commit()
    conn.close()


def get_document(doc_id):
    conn = create_conn()
    doc = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id, )).fetchone()
    conn.close()
    return dict(doc) if doc else None


def get_order(order_id):
    conn = create_conn()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id, )).fetchone()
    conn.close()
    return dict(order) if order else None

def get_user(token):
    conn = create_conn()
    user = conn.execute("SELECT * FROM users WHERE token = ?", (token, )).fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    conn = create_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]


def get_all_orders():
    conn = create_conn()
    try:
        rows = conn.execute("SELECT * FROM orders").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def create_order(owner_id, item, amount):
    conn = create_conn()
    try:
        cursor = conn.execute(
            """INSERT INTO orders (owner_id, item, amount)
               VALUES (?, ?, ?)""",
            (owner_id, item, amount)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_order(order_id, item, amount):
    conn = create_conn()
    try:
        cursor = conn.execute(
            """UPDATE orders SET item = ?, amount = ?
               WHERE id = ?""",
            (item, amount, order_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_order(order_id):
    conn = create_conn()
    try:
        cursor = conn.execute(
            "DELETE FROM orders WHERE id = ?",
            (order_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_all_documents():
    conn = create_conn()
    try:
        rows = conn.execute("SELECT * FROM documents").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def create_document(owner_id, title, content):
    conn = create_conn()
    try:
        cursor = conn.execute(
            """INSERT INTO documents (owner_id, title, content)
               VALUES (?, ?, ?)""",
            (owner_id, title, content)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_document(doc_id, title, content):
    conn = create_conn()
    try:
        cursor = conn.execute(
            """UPDATE documents SET title = ?, content = ?
               WHERE id = ?""",
            (title, content, doc_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_document(doc_id):
    conn = create_conn()
    try:
        cursor = conn.execute(
            "DELETE FROM documents WHERE id = ?",
            (doc_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
