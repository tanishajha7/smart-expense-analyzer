import csv
import matplotlib.pyplot as plt
from collections import defaultdict

FILENAME = "expenses.csv"

def read_expenses():
    expenses = []
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)
    return expenses

def category_summary():
    expenses = read_expenses()
    summary = defaultdict(float)

    for expense in expenses:
        summary[expense["Category"]] += float(expense["Amount"])

    return summary

def show_summary():
    summary = category_summary()

    print("\nCategory Wise Spending:")
    for category, amount in summary.items():
        print(f"{category}: ₹{amount}")

    highest = max(summary, key=summary.get)
    print(f"\nHighest Spending Category: {highest}")

def show_graph():
    summary = category_summary()

    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Expense Analysis")
    plt.show()