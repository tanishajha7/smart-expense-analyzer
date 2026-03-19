# 💰 Smart Expense Analyzer

A personal expense tracking web application built with **Python** and **HTML/CSS/JavaScript**.  
Developed by **Tanisha Jha** | BCA 2nd Year

---

## 🖥️ Live Demo

Open `index.html` directly in your browser — no installation needed!

---

## 📌 About the Project

Smart Expense Analyzer is a full-stack expense tracking tool that helps users record, categorize, and visualize their daily spending. It was built as a personal project to learn Python file handling, data analysis, and web development.

---

## ✨ Features

- ➕ Add expenses with date, category and amount
- 📋 View all transactions with live search/filter
- 📊 Visual charts — Pie chart and Bar chart
- 🏷️ Category-wise spending breakdown
- 💾 Data saved automatically in browser (localStorage)
- 🎨 Clean dark-themed responsive UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Logic | Python 3 |
| Data Storage | CSV file + localStorage |
| Data Analysis | Python `csv` module, `collections` |
| Charts | Matplotlib (Python), Chart.js (Web) |
| Web Frontend | HTML5, CSS3, JavaScript |
| Icons | Bootstrap Icons |
| Fonts | Google Fonts (Plus Jakarta Sans) |

---

## 📁 Project Structure

```
smart_expense_analyzer/
│
├── main.py              → Terminal-based menu app
├── expense_manager.py   → Handles saving expenses to CSV
├── analyzer.py          → Reads CSV, calculates summaries, draws charts
├── database.py          → Database module
├── expenses.csv         → Local data storage file
├── index.html           → Web version (open in browser)
└── README.md            → Project documentation
```

---

## 🚀 How to Run

### Web Version (Recommended)
```
Just double-click index.html — opens in your browser!
```

### Python Terminal Version
```bash
# Make sure Python is installed
python main.py
```

### Requirements for Python version
```bash
pip install matplotlib
```

---

## 📷 Screenshots

> Dashboard showing total spending, transaction count, top category and recent entries.

> Charts page with doughnut chart and bar chart breakdown by category.

*(Add screenshots of your running app here!)*

---

## 💡 What I Learned

- Python file handling with `csv` module
- Data analysis using `collections.defaultdict`
- Building data visualizations with `matplotlib`
- Frontend development with HTML, CSS and JavaScript
- How to connect Python logic with a web interface
- Version control with Git and GitHub

---

## 🔮 Future Improvements

- [ ] Add monthly budget limit alerts
- [ ] Export report as PDF
- [ ] Add login/user authentication
- [ ] Deploy online using GitHub Pages
- [ ] Connect to a real database (SQLite/PostgreSQL)

---

## 👩‍💻 Author

**Tanisha Jha**  
BCA Student | 2nd Year  
📧 Connect on [LinkedIn](#) | ⭐ Star this repo if you found it helpful!

---

*Built with 💜 as part of my FAANG preparation journey*
