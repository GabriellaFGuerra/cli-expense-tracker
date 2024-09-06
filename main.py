import sys

if sys.version_info < (3, 10):
    from importlib_resources import files
else:
    from importlib.resources import files

import json
import os
from datetime import datetime
import cmd
import argparse

EXPENSES_FILE = "expenses.json"


def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    else:
        return []


def save_expenses(expenses):
    try:
        with open(EXPENSES_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
    except Exception as e:
        print(f"Error saving expenses: {e}")


def add_expense(description, amount, category, date):
    expenses = load_expenses()
    expenses.append(
        {
            "description": description,
            "amount": amount,
            "category": category,
            "date": date,
        }
    )
    save_expenses(expenses)
    print("Expense added successfully!")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
    else:
        for idx, expense in enumerate(expenses, start=1):
            print(
                f"{idx}. {expense['description']} - ${expense['amount']} on {expense['date']} (Category: {expense['category']})"
            )


def search_expenses(query):
    expenses = load_expenses()
    filtered_expenses = [
        expense
        for expense in expenses
        if query.lower() in expense["description"].lower()
        or query.lower() in expense["category"].lower()
        or query in expense["date"]
    ]
    if not filtered_expenses:
        print("No expenses found.")
    else:
        for idx, expense in enumerate(filtered_expenses, 1):
            print(
                f"{idx}. {expense['description']} - {expense['amount']} - {expense['category']} - {expense['date']}"
            )


def calculate_expenses():
    expenses = load_expenses()
    total_expenses = sum(float(expense["amount"]) for expense in expenses)
    print(f"Total expenses: ${total_expenses:.2f}")


def delete_expense(idx):
    expenses = load_expenses()
    if idx < 1 or idx > len(expenses):
        print("Invalid expense index.")
    else:
        del expenses[idx - 1]
        save_expenses(expenses)
        print("Expense deleted successfully!")


def update_expense(idx, description, amount, category, date):
    expenses = load_expenses()
    if idx < 1 or idx > len(expenses):
        print("Invalid expense index.")
    else:
        expense = expenses[idx - 1]
        expense["description"] = description
        expense["amount"] = amount
        expense["category"] = category
        expense["date"] = date
        save_expenses(expenses)
        print("Expense updated successfully!")


def summarize_expenses():
    """View a summary of all expenses."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize.")
        return

    summary = {}
    for expense in expenses:
        category = expense["category"]
        amount = float(expense["amount"])
        summary[category] = summary.get(category, 0) + amount

    print("Summary of all expenses by category:")
    for category, total in summary.items():
        print(f"- {category}: ${total:.2f}")

    total_expenses = sum(float(expense["amount"]) for expense in expenses)
    print(f"Total expenses: ${total_expenses:.2f}")


def summarize_expenses_by_month(month):
    """View a summary of expenses for a specific month (of current year)."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize.")
        return

    current_year = datetime.now().year
    filtered_expenses = [
        expense
        for expense in expenses
        if datetime.strptime(expense["date"], "%Y-%m-%d").year == current_year
        and datetime.strptime(expense["date"], "%Y-%m-%d").month == month
    ]

    if not filtered_expenses:
        print(f"No expenses found for month {month} of {current_year}.")
        return

    summary = {}
    for expense in filtered_expenses:
        category = expense["category"]
        amount = float(expense["amount"])
        summary[category] = summary.get(category, 0) + amount

    print(
        f"Summary of expenses for {datetime(current_year, month, 1).strftime('%B %Y')}:"
    )
    for category, total in summary.items():
        print(f"- {category}: ${total:.2f}")

    total_expenses = sum(float(expense["amount"]) for expense in filtered_expenses)
    print(f"Total expenses for month {month}: ${total_expenses:.2f}")


class ExpenseCLI(cmd.Cmd):
    intro = "Welcome to Expense Tracker. Type ? to list commands.\n"
    prompt = "ExpenseTracker > "

    def do_add(self, args):
        """Add an expense: add <description> <amount> <category> <date>"""
        args = args.split(maxsplit=3)
        if len(args) != 4:
            print("Usage: add <description> <amount> <category> <date>")
        else:
            description = args[0]
            amount = float(args[1].replace(',', '.'))  # Replace comma with dot
            category = args[2]
            date = args[3]
            add_expense(description, amount, category, date)
            
    def do_list(self, args):
        """List all expenses: list"""
        list_expenses()

    def do_search(self, args):
        """Search expenses: search <query>"""
        if args:
            search_expenses(args)
        else:
            print("Usage: search <query>")

    def do_calculate(self, args):
        """Calculate total expenses: calculate"""
        calculate_expenses()

    def do_delete(self, args):
        """Delete an expense: delete <index>"""
        try:
            idx = int(args)
            delete_expense(idx)
        except ValueError:
            print("Usage: delete <index>")

    def do_update(self, args):
        """Update an expense: update <index> <description> <amount> <category> <date>"""
        try:
            args = args.split(maxsplit=5)
            if len(args) != 5:
                print("Usage: update <index> <description> <amount> <category> <date>")
            else:
                idx = int(args[0])
                description, amount, category, date = args[1:]
                update_expense(idx, description, float(amount), category, date)
        except ValueError:
            print("Error: Invalid amount or index.")

    def do_summarize(self, args):
        """Summarize all expenses by category: summarize"""
        summarize_expenses()

    def do_summarize_month(self, args):
        """Summarize expenses for a specific month: summarize_month <month_number>"""
        try:
            if not args:
                print("Usage: summarize_month <month_number>")
                return
            month = int(args.strip())
            if 1 <= month <= 12:
                summarize_expenses_by_month(month)
            else:
                print("Error: Month must be between 1 and 12.")
        except ValueError:
            print("Error: Invalid month entered.")

    def do_quit(self, args):
        """Quit the program: quit"""
        print("Exiting...")
        return True


def cli():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    parser.add_argument(
        "--add",
        nargs=4,
        metavar=("description", "amount", "category", "date"),
        help="Add an expense",
    )
    parser.add_argument("--list", action="store_true", help="List all expenses")
    parser.add_argument(
        "--search",
        metavar="query",
        help="Search expenses",
    )
    parser.add_argument(
        "--calculate",
        action="store_true",
        help="Calculate total expenses",
    )
    parser.add_argument(
        "--delete",
        metavar="index",
        help="Delete an expense",
    )
    parser.add_argument(
        "--update",
        nargs=5,
        metavar=("index", "description", "amount", "category", "date"),
        help="Update an expense",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Summarize all expenses by category",
    )
    parser.add_argument(
        "--summarize-month",
        metavar="month",
        type=int,
        help="Summarize expenses for a specific month (1-12)",
    )

    args = parser.parse_args()

    # Use match-case if using Python 3.10+, else use if-elif
    if args.add:
        description, amount, category, date = args.add
        add_expense(description, amount, category, date)
    elif args.list:
        list_expenses()
    elif args.search:
        search_expenses(args.search)
    elif args.calculate:
        calculate_expenses()
    elif args.delete:
        try:
            delete_expense(int(args.delete))
        except ValueError:
            print("Error: Invalid index entered.")
    elif args.update:
        idx, description, amount, category, date = args.update
        try:
            update_expense(int(idx), description, amount, category, date)
        except ValueError:
            print("Error: Invalid index entered.")
    elif args.summarize:
        summarize_expenses()
    elif args.summarize_month:
        month = args.summarize_month
        if 1 <= month <= 12:
            summarize_expenses_by_month(month)
        else:
            print("Error: Month must be between 1 and 12.")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
