import matplotlib.pyplot as plt
from collections import defaultdict
from .transactions import get_transactions_for_month
from datetime import datetime

def expense_pie_figure(year=None, month=None):
    rows = get_transactions_for_month(year, month)
    categories = defaultdict(float)
    for r in rows:
        if r["type"] == "Expense":
            categories[r["category"]] += r["amount"]
    fig, ax = plt.subplots(figsize=(5,5))
    if not categories:
        ax.text(0.5, 0.5, "No expenses yet", ha="center", va="center")
        ax.axis("off")
        return fig
    labels = list(categories.keys())
    sizes = list(categories.values())
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    title = "Expenses by Category"
    if year and month:
        title += f" — {year}-{month:02d}"
    ax.set_title(title)
    return fig

def income_vs_expense_figure(year=None, month=None):
    rows = get_transactions_for_month(year, month)
    income = sum(r["amount"] for r in rows if r["type"] == "Income")
    expense = sum(r["amount"] for r in rows if r["type"] == "Expense")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(["Income", "Expense"], [income, expense], color=["#2ca02c", "#d62728"])
    title = "Income vs Expense"
    if year and month:
        title += f" — {year}-{month:02d}"
    ax.set_title(title)
    return fig
