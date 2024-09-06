# Expense Tracker CLI
=======================

A simple command-line interface for tracking expenses.

## Prerequisites
-----------------

* Python 3.10+
* Git

## Installation
---------------

1. Clone this repository: `git clone https://github.com/your-username/expense-tracker-cli.git`
2. Navigate to the project directory: `cd expense-tracker-cli`
3. Install dependencies: `pip install -r requirements.txt`

## Usage

### Commands

* `add`: Add a new expense
    + Usage: `add <description> <amount> <category> <date>`
    + Example: `add "Lunch at restaurant" 15.99 "Food" "2023-02-20"`
* `list`: List all expenses
    + Usage: `list`
* `search`: Search for expenses by keyword
    + Usage: `search <query>`
    + Example: `search "restaurant"`
* `calculate`: Calculate total expenses
    + Usage: `calculate`
* `delete`: Delete an expense by index
    + Usage: `delete <index>`
    + Example: `delete 1`
* `update`: Update an expense by index
    + Usage: `update <index> <description> <amount> <category> <date>`
    + Example: `update 1 "New description" 10.99 "New category" "2023-02-21"`
* `summarize`: Summarize all expenses by category
    + Usage: `summarize`
* `summarize_month`: Summarize expenses for a specific month (1-12)
    + Usage: `summarize_month <month>`
    + Example: `summarize_month 2`

### Options

* `-h` or `--help`: Show this help message and exit

## Example Use Cases
--------------------

* Add a new expense: `add "Groceries" 50.00 "Shopping" "2023-02-15"`
* List all expenses: `list`
* Search for expenses containing "restaurant": `search "restaurant"`
* Calculate total expenses: `calculate`
* Delete the first expense: `delete 1`
* Update the second expense: `update 2 "New description" 20.00 "New category" "2023-02-22"`

## Running the CLI
------------------

1. Clone this repository: `git clone https://github.com/your-username/expense-tracker-cli.git`
2. Navigate to the project directory: `cd expense-tracker-cli`
3. Run the CLI: `python main.py`

Note: This project uses Python 3.10+. If you're using an earlier version, you may need to modify the code to use `if-elif` statements instead of `match-case`.

## Source
[Roadmap.sh](https://roadmap.sh/projects/expense-tracker)