import tkinter as tk
from tkinter import ttk, messagebox
from app.transactions import add_transaction, get_summary_for_month, get_overall_summary, load_transactions
from app.charts import plot_expense_pie_for_month, plot_income_vs_expense_for_month
from app.goals import add_goal, load_goals, update_goal_saved
from datetime import datetime
import calendar

def parse_date_input(s):
    # Accept YYYY-MM-DD or empty -> today
    if not s.strip():
        return datetime.today().date().isoformat()
    try:
        return datetime.fromisoformat(s).date().isoformat()
    except Exception:
        return None

root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("900x600")

# Notebook (tabs)
nb = ttk.Notebook(root)
tab_dashboard = ttk.Frame(nb)
tab_transactions = ttk.Frame(nb)
tab_goals = ttk.Frame(nb)
tab_charts = ttk.Frame(nb)
nb.add(tab_dashboard, text="Dashboard")
nb.add(tab_transactions, text="Transactions")
nb.add(tab_goals, text="Savings Goals")
nb.add(tab_charts, text="Charts")
nb.pack(expand=1, fill="both")

# ---------- Dashboard Tab ----------
dash_frame = ttk.Frame(tab_dashboard, padding=10)
dash_frame.pack(fill="both", expand=True)

# Monthly summary controls
month_label = ttk.Label(dash_frame, text="Select month (YYYY-MM):")
month_label.grid(row=0, column=0, sticky="w")
month_entry = ttk.Entry(dash_frame)
month_entry.grid(row=0, column=1, sticky="w")
month_entry.insert(0, datetime.today().strftime("%Y-%m"))

def update_dashboard():
    mval = month_entry.get().strip()
    try:
        year, month = map(int, mval.split("-"))
    except Exception:
        messagebox.showwarning("Input Error", "Enter month as YYYY-MM")
        return
    income, expense, balance = get_summary_for_month(year, month)
    income_var.set(f"${income:.2f}")
    expense_var.set(f"${expense:.2f}")
    balance_var.set(f"${balance:.2f}")

    # show recent transactions list
    for widget in recent_tree.get_children():
        recent_tree.delete(widget)
    transactions = load_transactions()
    # show only last 20 for readability
    for t in transactions[-20:][::-1]:
        recent_tree.insert("", "end", values=(t["date"], t["category"], t["type"], f"${t['amount']:.2f}"))

# Summary labels
income_var = tk.StringVar()
expense_var = tk.StringVar()
balance_var = tk.StringVar()

ttk.Label(dash_frame, text="Income:").grid(row=1, column=0, sticky="w", pady=5)
ttk.Label(dash_frame, textvariable=income_var).grid(row=1, column=1, sticky="w")
ttk.Label(dash_frame, text="Expenses:").grid(row=2, column=0, sticky="w")
ttk.Label(dash_frame, textvariable=expense_var).grid(row=2, column=1, sticky="w")
ttk.Label(dash_frame, text="Balance:").grid(row=3, column=0, sticky="w")
ttk.Label(dash_frame, textvariable=balance_var).grid(row=3, column=1, sticky="w")

# recent transactions treeview
recent_tree = ttk.Treeview(dash_frame, columns=("date","category","type","amount"), show="headings", height=10)
recent_tree.heading("date", text="Date")
recent_tree.heading("category", text="Category")
recent_tree.heading("type", text="Type")
recent_tree.heading("amount", text="Amount")
recent_tree.grid(row=4, column=0, columnspan=4, pady=10, sticky="nsew")

ttk.Button(dash_frame, text="Refresh", command=update_dashboard).grid(row=0, column=2, padx=10)

# ---------- Transactions Tab ----------
tr_frame = ttk.Frame(tab_transactions, padding=10)
tr_frame.pack(fill="both", expand=True)

ttk.Label(tr_frame, text="Amount:").grid(row=0, column=0, sticky="w")
entry_amount = ttk.Entry(tr_frame)
entry_amount.grid(row=0, column=1, sticky="w")

ttk.Label(tr_frame, text="Category:").grid(row=1, column=0, sticky="w")
entry_category = ttk.Entry(tr_frame)
entry_category.grid(row=1, column=1, sticky="w")

ttk.Label(tr_frame, text="Type:").grid(row=2, column=0, sticky="w")
combo_type = ttk.Combobox(tr_frame, values=["Income","Expense"], state="readonly")
combo_type.current(1)
combo_type.grid(row=2, column=1, sticky="w")

ttk.Label(tr_frame, text="Date (YYYY-MM-DD) optional:").grid(row=3, column=0, sticky="w")
entry_date = ttk.Entry(tr_frame)
entry_date.grid(row=3, column=1, sticky="w")

def on_add_transaction():
    amount = entry_amount.get().strip()
    category = entry_category.get().strip()
    ttype = combo_type.get()
    d = parse_date_input(entry_date.get())
    if not amount or not category:
        messagebox.showwarning("Input Error", "Enter amount and category")
        return
    try:
        float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number")
        return
    add_transaction(amount, category, ttype, d)
    entry_amount.delete(0,tk.END)
    entry_category.delete(0,tk.END)
    entry_date.delete(0,tk.END)
    messagebox.showinfo("Success", "Transaction added")
    update_dashboard()

ttk.Button(tr_frame, text="Add Transaction", command=on_add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

# ---------- Goals Tab ----------
go_frame = ttk.Frame(tab_goals, padding=10)
go_frame.pack(fill="both", expand=True)

ttk.Label(go_frame, text="Goal name:").grid(row=0, column=0, sticky="w")
entry_goal_name = ttk.Entry(go_frame)
entry_goal_name.grid(row=0, column=1, sticky="w")
ttk.Label(go_frame, text="Goal amount:").grid(row=1, column=0, sticky="w")
entry_goal_amt = ttk.Entry(go_frame)
entry_goal_amt.grid(row=1, column=1, sticky="w")

def on_add_goal():
    name = entry_goal_name.get().strip()
    amt = entry_goal_amt.get().strip()
    if not name or not amt:
        messagebox.showwarning("Input Error", "Enter name and amount")
        return
    try:
        float(amt)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number")
        return
    add_goal(name, amt)
    entry_goal_name.delete(0, tk.END)
    entry_goal_amt.delete(0, tk.END)
    update_goals_view()

ttk.Button(go_frame, text="Add Goal", command=on_add_goal).grid(row=2, column=0, columnspan=2, pady=6)

goals_container = ttk.Frame(go_frame)
goals_container.grid(row=3, column=0, columnspan=2, pady=10)

def update_goals_view():
    for w in goals_container.winfo_children():
        w.destroy()
    goals = load_goals()
    for i,g in enumerate(goals):
        ttk.Label(goals_container, text=g["name"]).grid(row=i, column=0, sticky="w")
        prog = ttk.Progressbar(goals_container, length=300, maximum=g["amount"], value=g["saved"])
        prog.grid(row=i, column=1, padx=5, pady=3)
        ttk.Label(goals_container, text=f"${g['saved']:.2f} / ${g['amount']:.2f}").grid(row=i, column=2)

update_goals_view()

# ---------- Charts Tab ----------
ch_frame = ttk.Frame(tab_charts, padding=10)
ch_frame.pack(fill="both", expand=True)

ttk.Label(ch_frame, text="Select month for charts (YYYY-MM):").grid(row=0, column=0, sticky="w")
chart_month_entry = ttk.Entry(ch_frame)
chart_month_entry.grid(row=0, column=1, sticky="w")
chart_month_entry.insert(0, datetime.today().strftime("%Y-%m"))

def show_pie():
    m = chart_month_entry.get().strip()
    try:
        y,mn = map(int, m.split("-"))
    except Exception:
        messagebox.showwarning("Input Error", "Enter YYYY-MM")
        return
    plot_expense_pie_for_month(y, mn)

def show_bar():
    m = chart_month_entry.get().strip()
    try:
        y,mn = map(int, m.split("-"))
    except Exception:
        messagebox.showwarning("Input Error", "Enter YYYY-MM")
        return
    plot_income_vs_expense_for_month(y, mn)

ttk.Button(ch_frame, text="Show Expense Pie", command=show_pie).grid(row=1, column=0, pady=8)
ttk.Button(ch_frame, text="Show Income vs Expense", command=show_bar).grid(row=1, column=1, pady=8)

# Initialize
update_dashboard()
root.mainloop()
