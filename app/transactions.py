from .db import get_conn
from datetime import datetime
from typing import List, Dict

def add_transaction(amount: float, category: str, ttype: str, date_str: str, note: str = ""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (amount, category, type, date, note) VALUES (?, ?, ?, ?, ?)",
        (float(amount), category, ttype, date_str, note)
    )
    conn.commit()
    conn.close()

def get_transactions(limit: int = 500) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_transactions_for_month(year: int, month: int):
    conn = get_conn()
    cur = conn.cursor()
    start = f"{year:04d}-{month:02d}-01"
    # naive end: next month first day
    if month == 12:
        end = f"{year+1:04d}-01-01"
    else:
        end = f"{year:04d}-{month+1:02d}-01"
    cur.execute("""
        SELECT * FROM transactions
        WHERE date >= ? AND date < ?
        ORDER BY date ASC
    """, (start, end))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_summary_for_month(year: int, month: int):
    rows = get_transactions_for_month(year, month)
    income = sum(r["amount"] for r in rows if r["type"] == "Income")
    expense = sum(r["amount"] for r in rows if r["type"] == "Expense")
    return income, expense, income - expense

def get_overall_summary():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) as s FROM transactions WHERE type = 'Income'")
    income = cur.fetchone()["s"] or 0.0
    cur.execute("SELECT SUM(amount) as s FROM transactions WHERE type = 'Expense'")
    expense = cur.fetchone()["s"] or 0.0
    conn.close()
    return income, expense, income - expense
