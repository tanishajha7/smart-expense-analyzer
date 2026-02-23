from expense_manager import initialize_file, add_expense
from analyzer import show_summary, show_graph
from datetime import datetime

initialize_file()

while True:
    print("\n===== Smart Expense Analyzer =====")
    print("1. Add Expense")
    print("2. Show Summary")
    print("3. Show Graph")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        date = datetime.now().strftime("%d-%m-%Y")
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        add_expense(date, category, amount)
        print("Expense Added Successfully!")

    elif choice == "2":
        show_summary()

    elif choice == "3":
        show_graph()

    elif choice == "4":
        break

    else:
        print("Invalid choice!")