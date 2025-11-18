from .db import get_conn
from typing import List, Dict

def add_goal(name: str, target_amount: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO goals (name, target_amount, saved_amount) VALUES (?, ?, 0)", (name, float(target_amount)))
    conn.commit()
    conn.close()

def get_goals() -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM goals ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def update_goal_saved(goal_id: int, saved_amount: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE goals SET saved_amount = ? WHERE id = ?", (float(saved_amount), int(goal_id)))
    conn.commit()
    conn.close()

def delete_goal(goal_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM goals WHERE id = ?", (int(goal_id),))
    conn.commit()
    conn.close()
