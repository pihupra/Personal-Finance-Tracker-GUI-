

# **💰 Personal Finance Tracker (Python GUI – Tkinter + Matplotlib)**

A beautiful and simple desktop application to manage your **income, expenses, and savings goals**, complete with charts, progress bars, and automatic data saving.

---

## 🚀 **Project Overview**

The **Personal Finance Tracker** is a Python GUI-based application designed to help users stay on top of their financial activities.
Whether you want to track your spending, monitor income sources, or stay committed to monthly savings goals — this app provides everything in one clean interface.

It is built using:

* 🖥 **Tkinter** for the graphical user interface
* 📊 **Matplotlib** for charts
* 📁 **JSON** for persistent data storage

Simple enough for beginners, practical enough for daily real-world use.

---

## ✨ **Features**

### ✅ **Add Income & Expenses**

* Enter amount, category, and description
* Automatically saved
* Easy to edit later

### 📊 **Built-in Analytics Dashboard**

* View monthly financial summaries
* Spending vs earning charts
* Category-wise bar graphs
* Visual breakdown using Matplotlib

### 🎯 **Savings Goal Tracker**

* Define your monthly or yearly savings goal
* See visual **progress bars**
* Stay motivated to hit your targets

### 💾 **Persistent Storage**

* All data is saved in a `finance_data.json` file
* No database setup required
* Your data remains safe even after closing the app

### 🎨 **Clean & Beginner-Friendly UI**

* Simple Tkinter dashboard
* Intuitive, modern layout
* Works on Windows, Mac, and Linux (outside Codespaces)

---

## 🧪 **Tech Stack**

| Technology | Purpose            |
| ---------- | ------------------ |
| Python     | Main language      |
| Tkinter    | GUI framework      |
| Matplotlib | Graphs & charts    |
| JSON       | Local data storage |

---

## 📂 **Project Structure**

```
📦 Personal-Finance-Tracker
├── main.py                # Main GUI application
├── finance_manager.py     # Logic for saving/reading data
├── charts.py              # Chart-generation functions
├── finance_data.json      # Auto-created saved data file
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## ▶️ **How to Run the Project (Local Computer)**

### **1) Install Python**

Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### **2) Install required libraries**

```bash
pip install -r requirements.txt
```

### **3) Run the app**

```bash
python main.py
```

---

## 🧑‍💻 **Running in GitHub Codespaces (without GUI)**

⚠️ **Tkinter does NOT work in GitHub Codespaces**, because there is no GUI display.

To run it properly:

### **✔ Option 1: Clone the repo locally**

1. Install Python
2. Install VS Code
3. Clone the repo
4. Run `python main.py`

### **✔ Option 2: Use a local virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python main.py
```

---

## 📈 **Future Improvements**

Here are some enhancements planned for upcoming versions:

* Add export to CSV / Excel
* Monthly spending heatmap
* Notifications for overspending
* Multiple user profiles

Feel free to contribute!

---

## 🤝 **Contributing**

Pull requests are welcome!
If you want to add features or fix bugs:

1. Fork the repo
2. Create a new branch
3. Commit your changes
4. Submit a PR

---

## 📜 **License**

This project is licensed under the **MIT License** — free to use and modify.

---

## ⭐ **Support the Project**

If you find this project useful, consider giving the repo a **star** ⭐.
It helps others discover it!

