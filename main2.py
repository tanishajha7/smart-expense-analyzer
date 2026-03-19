from database import initialize_db, add_expense, get_expenses, delete_expense
from datetime import datetime

initialize_db()

while True:
    print("\n===== Smart Expense Tracker (Database Version) =====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Delete Expense")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        date = datetime.now().strftime("%d-%m-%Y")
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        add_expense(date, category, amount)
        print("✅ Expense Added Successfully!")

    elif choice == "2":
        expenses = get_expenses()
        print("\nID | Date | Category | Amount")
        print("--------------------------------")
        for exp in expenses:
            print(f"{exp[0]} | {exp[1]} | {exp[2]} | ₹{exp[3]}")

    elif choice == "3":
        expense_id = int(input("Enter Expense ID to delete: "))
        delete_expense(expense_id)
        print("🗑 Expense Deleted!")

    elif choice == "4":
        break

    else:
        print("Invalid choice!")