import sqlite3
from pathlib import Path

DB_PATH = Path("data/finance.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # transactions: id, amount, category, type, date, note
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL,    -- Income or Expense
        date TEXT NOT NULL,    -- ISO date YYYY-MM-DD
        note TEXT
    )
    """)
    # goals: id, name, target_amount, saved_amount
    cur.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        target_amount REAL NOT NULL,
        saved_amount REAL NOT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# Auto init on import
init_db()
