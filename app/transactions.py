from pathlib import Path
import json
from datetime import date, datetime

DATA_FILE = Path("data/transactions.json")
DATA_FILE.parent.mkdir(exist_ok=True)

def load_transactions():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_transactions(transactions):
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4, default=str)

def add_transaction(amount, category, trans_type, trans_date=None):
    transactions = load_transactions()
    if trans_date is None:
        trans_date = date.today().isoformat()
    # allow supplied date string or object
    if isinstance(trans_date, (datetime, date)):
        trans_date = trans_date.isoformat()
    transactions.append({
        "amount": float(amount),
        "category": category,
        "type": trans_type,  # 'Income' or 'Expense'
        "date": trans_date
    })
    save_transactions(transactions)

def get_summary_for_month(year:int, month:int):
    """Return (income, expense, balance) for a given year/month."""
    transactions = load_transactions()
    income = 0.0
    expense = 0.0
    for t in transactions:
        d = datetime.fromisoformat(t["date"])
        if d.year == year and d.month == month:
            if t["type"] == "Income":
                income += t["amount"]
            else:
                expense += t["amount"]
    return income, expense, income - expense

def get_overall_summary():
    transactions = load_transactions()
    income = sum(t["amount"] for t in transactions if t["type"]=="Income")
    expense = sum(t["amount"] for t in transactions if t["type"]=="Expense")
    return income, expense, income - expense
