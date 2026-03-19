import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime

# ── reuse your existing logic ────────────────────────────────────
FILENAME = "expenses.csv"

def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as f:
            csv.writer(f).writerow(["Date", "Category", "Amount"])

def add_expense(date, category, amount):
    with open(FILENAME, "a", newline="") as f:
        csv.writer(f).writerow([date, category, amount])

def read_expenses():
    expenses = []
    with open(FILENAME, "r") as f:
        for row in csv.DictReader(f):
            expenses.append(row)
    return expenses

def category_summary():
    summary = defaultdict(float)
    for e in read_expenses():
        summary[e["Category"]] += float(e["Amount"])
    return summary

# ── colour palette ───────────────────────────────────────────────
BG       = "#F8F9FA"
SIDEBAR  = "#1A73E8"
WHITE    = "#FFFFFF"
TEXT     = "#202124"
ACCENT   = "#34A853"
RED      = "#EA4335"
BORDER   = "#DADCE0"
LIGHT    = "#E8F0FE"

FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_H   = ("Segoe UI", 14, "bold")
FONT_BIG = ("Segoe UI", 22, "bold")

# ════════════════════════════════════════════════════════════════
class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        initialize_file()
        self.title("Smart Expense Analyzer")
        self.geometry("950x620")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()
        self.show_frame("Dashboard")

    # ── layout ──────────────────────────────────────────────────
    def _build_ui(self):
        # sidebar
        sidebar = tk.Frame(self, bg=SIDEBAR, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="💰", font=("Segoe UI", 28),
                 bg=SIDEBAR, fg=WHITE).pack(pady=(28, 4))
        tk.Label(sidebar, text="Expense\nAnalyzer", font=("Segoe UI", 12, "bold"),
                 bg=SIDEBAR, fg=WHITE, justify="center").pack(pady=(0, 28))

        self.nav_btns = {}
        for page in ["Dashboard", "Add Expense", "All Expenses", "Charts"]:
            icon = {"Dashboard":"🏠","Add Expense":"➕",
                    "All Expenses":"📋","Charts":"📊"}[page]
            b = tk.Button(sidebar, text=f"  {icon}  {page}",
                          font=FONT, bg=SIDEBAR, fg=WHITE,
                          activebackground="#1558B0", activeforeground=WHITE,
                          bd=0, anchor="w", padx=16, pady=10, cursor="hand2",
                          command=lambda p=page: self.show_frame(p))
            b.pack(fill="x")
            self.nav_btns[page] = b

        # main area
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.frames = {}
        name_map = {
            Dashboard:   "Dashboard",
            AddExpense:  "Add Expense",
            AllExpenses: "All Expenses",
            Charts:      "Charts",
        }
        for F in [Dashboard, AddExpense, AllExpenses, Charts]:
            frame = F(self.main, self)
            self.frames[name_map[F]] = frame
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, name):
        for n, b in self.nav_btns.items():
            b.configure(bg="#1558B0" if n == name else SIDEBAR)
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

# ════════════════════════════════════════════════════════════════
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="Dashboard", font=FONT_H,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(22,14))

        self.cards_frame = tk.Frame(self, bg=BG)
        self.cards_frame.pack(fill="x", padx=24)

        self.summary_frame = tk.Frame(self, bg=WHITE, relief="flat",
                                       highlightbackground=BORDER, highlightthickness=1)
        self.summary_frame.pack(fill="both", expand=True, padx=24, pady=14)

    def refresh(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()
        for w in self.summary_frame.winfo_children():
            w.destroy()

        expenses = read_expenses()
        total    = sum(float(e["Amount"]) for e in expenses)
        summary  = category_summary()
        highest  = max(summary, key=summary.get) if summary else "N/A"
        count    = len(expenses)

        cards = [
            ("Total Spent",    f"₹{total:,.2f}",       ACCENT),
            ("Transactions",   str(count),              SIDEBAR),
            ("Top Category",   highest,                 RED),
        ]
        for label, value, color in cards:
            c = tk.Frame(self.cards_frame, bg=WHITE, width=190, height=90,
                         highlightbackground=color, highlightthickness=2)
            c.pack(side="left", padx=8, pady=4)
            c.pack_propagate(False)
            tk.Label(c, text=value, font=FONT_BIG, bg=WHITE, fg=color).pack(pady=(14,2))
            tk.Label(c, text=label, font=FONT,     bg=WHITE, fg="#5F6368").pack()

        # recent 5
        tk.Label(self.summary_frame, text="Recent Expenses",
                 font=FONT_B, bg=WHITE, fg=TEXT).pack(anchor="w", padx=14, pady=(10,4))

        cols = ("Date", "Category", "Amount")
        tree = ttk.Treeview(self.summary_frame, columns=cols,
                            show="headings", height=6)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=200, anchor="center")
        for e in reversed(expenses[-5:]):
            tree.insert("", "end", values=(e["Date"], e["Category"],
                                           f"₹{float(e['Amount']):,.2f}"))
        tree.pack(fill="x", padx=14, pady=(0,10))

# ════════════════════════════════════════════════════════════════
class AddExpense(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="Add New Expense", font=FONT_H,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(22,14))

        card = tk.Frame(self, bg=WHITE, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(padx=28, pady=4, fill="x")

        fields = [("Date (DD-MM-YYYY)", "date"), ("Category", "cat"), ("Amount (₹)", "amt")]
        self.vars = {}
        for label, key in fields:
            row = tk.Frame(card, bg=WHITE)
            row.pack(fill="x", padx=20, pady=8)
            tk.Label(row, text=label, font=FONT_B, bg=WHITE,
                     fg=TEXT, width=20, anchor="w").pack(side="left")
            var = tk.StringVar()
            self.vars[key] = var
            tk.Entry(row, textvariable=var, font=FONT, relief="solid",
                     bd=1, width=30).pack(side="left", padx=8)

        # preset today
        self.vars["date"].set(datetime.now().strftime("%d-%m-%Y"))

        # category suggestions
        cat_row = tk.Frame(card, bg=WHITE)
        cat_row.pack(fill="x", padx=20, pady=(0,8))
        tk.Label(cat_row, text="Quick Categories:", font=FONT,
                 bg=WHITE, fg="#5F6368").pack(side="left")
        for cat in ["Food", "Transport", "Shopping", "Bills", "Health"]:
            tk.Button(cat_row, text=cat, font=("Segoe UI", 9),
                      bg=LIGHT, fg=SIDEBAR, bd=0, padx=8, pady=4,
                      cursor="hand2",
                      command=lambda c=cat: self.vars["cat"].set(c)
                      ).pack(side="left", padx=4)

        self.msg = tk.Label(card, text="", font=FONT, bg=WHITE)
        self.msg.pack(pady=4)

        tk.Button(card, text="  ➕  Add Expense", font=FONT_B,
                  bg=ACCENT, fg=WHITE, relief="flat", padx=20, pady=10,
                  cursor="hand2", command=self._add).pack(pady=(4,16))

    def _add(self):
        date = self.vars["date"].get().strip()
        cat  = self.vars["cat"].get().strip()
        amt  = self.vars["amt"].get().strip()

        if not date or not cat or not amt:
            self.msg.config(text="⚠ Please fill all fields.", fg=RED)
            return
        try:
            amount = float(amt)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.msg.config(text="⚠ Enter a valid positive amount.", fg=RED)
            return

        add_expense(date, cat, amount)
        self.msg.config(text=f"✅ ₹{amount:,.2f} added under '{cat}'!", fg=ACCENT)
        self.vars["cat"].set("")
        self.vars["amt"].set("")

# ════════════════════════════════════════════════════════════════
class AllExpenses(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="All Expenses", font=FONT_H,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(22,4))

        # search bar
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=6)
        tk.Label(bar, text="Filter by category:", font=FONT,
                 bg=BG, fg=TEXT).pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *a: self.refresh())
        tk.Entry(bar, textvariable=self.filter_var, font=FONT,
                 relief="solid", bd=1, width=20).pack(side="left", padx=8)

        cols = ("Date", "Category", "Amount")
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=24, pady=4)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=220, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.total_label = tk.Label(self, text="", font=FONT_B, bg=BG, fg=ACCENT)
        self.total_label.pack(anchor="e", padx=28, pady=6)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        f = self.filter_var.get().lower()
        total = 0
        for e in read_expenses():
            if f in e["Category"].lower():
                amt = float(e["Amount"])
                total += amt
                self.tree.insert("", "end", values=(
                    e["Date"], e["Category"], f"₹{amt:,.2f}"))
        self.total_label.config(text=f"Total: ₹{total:,.2f}")

# ════════════════════════════════════════════════════════════════
class Charts(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.canvas_widget = None
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=24, pady=(18,6))
        tk.Label(top, text="Charts & Analysis", font=FONT_H,
                 bg=BG, fg=TEXT).pack(side="left")

        self.chart_var = tk.StringVar(value="Pie Chart")
        for opt in ["Pie Chart", "Bar Chart"]:
            tk.Radiobutton(top, text=opt, variable=self.chart_var,
                           value=opt, font=FONT, bg=BG, fg=TEXT,
                           command=self.refresh).pack(side="left", padx=10)

        self.chart_frame = tk.Frame(self, bg=WHITE,
                                     highlightbackground=BORDER,
                                     highlightthickness=1)
        self.chart_frame.pack(fill="both", expand=True, padx=24, pady=6)

    def refresh(self):
        for w in self.chart_frame.winfo_children():
            w.destroy()

        summary = category_summary()
        if not summary:
            tk.Label(self.chart_frame, text="No expenses yet. Add some first!",
                     font=FONT, bg=WHITE, fg="#5F6368").pack(expand=True)
            return

        cats   = list(summary.keys())
        amounts = list(summary.values())
        colors = ["#1A73E8","#34A853","#FBBC04","#EA4335",
                  "#9C27B0","#00BCD4","#FF5722","#607D8B"]

        fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=96)
        fig.patch.set_facecolor(WHITE)

        if self.chart_var.get() == "Pie Chart":
            ax.pie(amounts, labels=cats, autopct="%1.1f%%",
                   colors=colors[:len(cats)], startangle=140,
                   textprops={"fontsize": 9})
            ax.set_title("Spending by Category", fontsize=12, fontweight="bold")
        else:
            bars = ax.bar(cats, amounts, color=colors[:len(cats)],
                          edgecolor="white", linewidth=0.8)
            ax.set_xlabel("Category", fontsize=9)
            ax.set_ylabel("Amount (₹)", fontsize=9)
            ax.set_title("Category-wise Expenses", fontsize=12, fontweight="bold")
            ax.set_facecolor(BG)
            fig.patch.set_facecolor(WHITE)
            for bar, amt in zip(bars, amounts):
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + max(amounts)*0.01,
                        f"₹{amt:,.0f}", ha="center", va="bottom", fontsize=8)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ExpenseApp()
    app.mainloop()
