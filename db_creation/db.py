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