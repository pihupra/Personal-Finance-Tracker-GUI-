import streamlit as st
from datetime import date, datetime
from app import transactions, goals, charts
import pandas as pd

st.set_page_config(page_title="Personal Finance Tracker", layout="wide", initial_sidebar_state="expanded")

st.title("💰 Personal Finance Tracker")

# --- Sidebar navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Transaction", "Goals", "Charts", "Export"])

# Small helper to parse year-month
def parse_ym(s: str):
    try:
        y, m = map(int, s.split("-"))
        return y, m
    except Exception:
        today = datetime.today()
        return today.year, today.month

# --- Dashboard ---
if page == "Dashboard":
    st.header("📊 Monthly Summary")
    default_ym = datetime.today().strftime("%Y-%m")
    ym = st.text_input("Enter month (YYYY-MM)", value=default_ym)
    year, month = parse_ym(ym)
    income, expense, balance = transactions.get_summary_for_month(year, month)
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"${income:,.2f}")
    col2.metric("Expenses", f"${expense:,.2f}")
    col3.metric("Balance", f"${balance:,.2f}")

    st.subheader("Recent transactions")
    rows = transactions.get_transactions(limit=100)
    if rows:
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        st.dataframe(df)
    else:
        st.info("No transactions yet. Add one from 'Add Transaction'.")

    st.subheader("Goals progress")
    gs = goals.get_goals()
    if gs:
        for g in gs:
            pct = 0.0 if g["target_amount"] == 0 else min(1.0, g["saved_amount"]/g["target_amount"])
            st.write(f"**{g['name']}** — ${g['saved_amount']:.2f} / ${g['target_amount']:.2f}")
            st.progress(pct)
    else:
        st.info("No goals yet. Add one from 'Goals' tab.")

# --- Add Transaction ---
elif page == "Add Transaction":
    st.header("➕ Add a Transaction")
    with st.form("trans_form"):
        col1, col2 = st.columns(2)
        amount = col1.number_input("Amount (USD)", min_value=0.0, format="%.2f")
        ttype = col2.selectbox("Type", ["Expense", "Income"])
        category = st.text_input("Category (e.g., Food, Salary, Rent)")
        note = st.text_area("Note (optional)")
        date_input = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if amount <= 0 or not category.strip():
                st.error("Please enter a positive amount and a category.")
            else:
                transactions.add_transaction(amount, category.strip(), ttype, date_input.isoformat(), note.strip())
                st.success("Transaction added ✅")
                st.experimental_rerun()

# --- Goals ---
elif page == "Goals":
    st.header("🎯 Savings Goals")
    with st.expander("Add new goal"):
        with st.form("goal_form"):
            name = st.text_input("Goal name (e.g., Emergency Fund)")
            target = st.number_input("Target amount (USD)", min_value=0.0, format="%.2f")
            submit_goal = st.form_submit_button("Add Goal")
            if submit_goal:
                if not name.strip() or target <= 0:
                    st.error("Please provide a valid name and target.")
                else:
                    goals.add_goal(name.strip(), target)
                    st.success("New goal created ✅")
                    st.experimental_rerun()

    st.subheader("Manage goals")
    gs = goals.get_goals()
    if gs:
        for g in gs:
            st.write(f"**{g['name']}** — Target: ${g['target_amount']:.2f}")
            new_saved = st.number_input(f"Update saved for '{g['name']}'", min_value=0.0, value=float(g['saved_amount']), key=f"saved_{g['id']}")
            if st.button(f"Update saved ({g['name']})", key=f"upd_{g['id']}"):
                goals.update_goal_saved(g['id'], new_saved)
                st.success("Goal updated")
                st.experimental_rerun()
            if st.button(f"Delete {g['name']}", key=f"del_{g['id']}"):
                goals.delete_goal(g['id'])
                st.success("Goal deleted")
                st.experimental_rerun()
    else:
        st.info("No goals yet.")

# --- Charts ---
elif page == "Charts":
    st.header("📈 Charts")
    default_ym = datetime.today().strftime("%Y-%m")
    ym_chart = st.text_input("Month for charts (YYYY-MM)", value=default_ym)
    y, m = parse_ym(ym_chart)
    st.subheader("Expense breakdown (pie)")
    fig1 = charts.expense_pie_figure(y, m)
    st.pyplot(fig1)

    st.subheader("Income vs Expense")
    fig2 = charts.income_vs_expense_figure(y, m)
    st.pyplot(fig2)

# --- Export ---
elif page == "Export":
    st.header("📁 Export data")
    st.write("Download transactions as CSV")
    rows = transactions.get_transactions(limit=10000)
    if rows:
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="transactions.csv", mime="text/csv")
    else:
        st.info("No transactions to export.")
