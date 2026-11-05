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

def get_all_users():
    conn = create_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]