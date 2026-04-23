import datetime
import csv
import os
import json

class Expense:
    def __init__(self, name, category, amount, date=None):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date or datetime.date.today().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, Rs.{self.amount}>"

class FarmerExpenseTracker:
    def __init__(self):
        self.expense_file_path = "farmer_expenses.csv"
        self.categories_file_path = "farmer_categories.json"
        self.budget_file_path = "farmer_budget.txt"
        self.default_categories = [
            "Seeds & Planting", "Equipment & Machinery", "Irrigation & Water", "Fertilizers",
            "Pesticides & Chemicals", "Labor Costs", "Transportation", "Market & Selling",
            "Food & Personal", "Household", "Fuel & Energy", "Veterinary & Livestock",
            "Maintenance & Repairs", "Loan & Interest", "Communication", "Miscellaneous"
        ]
        self.load_categories()

    def load_categories(self):
        if os.path.exists(self.categories_file_path):
            try:
                with open(self.categories_file_path, 'r') as f:
                    self.categories = json.load(f)
            except:
                self.categories = self.default_categories.copy()
                self.save_categories()
        else:
            self.categories = self.default_categories.copy()
            self.save_categories()

    def save_categories(self):
        with open(self.categories_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.categories, f, indent=2)

    def add_expense(self, name, category, amount, date=None):
        if category not in self.categories:
            return {"status": "error", "error": "Invalid category"}
        try:
            amount = float(amount)
            if amount <= 0:
                return {"status": "error", "error": "Amount must be positive"}
        except ValueError:
            return {"status": "error", "error": "Invalid amount"}
        if date:
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {"status": "error", "error": "Invalid date format"}
        expense = Expense(name, category, amount, date)
        self.save_expense_to_file(expense)
        return {"status": "success", "message": f"Expense '{name}' saved successfully!"}

    def save_expense_to_file(self, expense):
        file_exists = os.path.exists(self.expense_file_path)
        with open(self.expense_file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Name', 'Amount', 'Category', 'Date'])
            writer.writerow([expense.name, expense.amount, expense.category, expense.date])

    def load_expenses(self):
        expenses = []
        if not os.path.exists(self.expense_file_path):
            return expenses
        try:
            with open(self.expense_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    expense = Expense(
                        name=row['Name'],
                        amount=float(row['Amount']),
                        category=row['Category'],
                        date=row['Date']
                    )
                    expenses.append(expense)
        except Exception:
            pass
        return expenses

    def get_summary(self, budget=None):
        expenses = self.load_expenses()
        summary = {"by_category": {}, "total_spent": 0, "budget": budget, "remaining": None, "daily_budget": None}

        if not expenses:
            return {"message": "No expenses recorded yet."}

        for exp in expenses:
            summary["by_category"].setdefault(exp.category, 0)
            summary["by_category"][exp.category] += exp.amount
            summary["total_spent"] += exp.amount

        if budget:
            remaining = budget - summary["total_spent"]
            summary["remaining"] = remaining
            if remaining > 0:
                now = datetime.datetime.now()
                days_in_month = (datetime.date(now.year, now.month % 12 + 1, 1) - datetime.timedelta(days=1)).day
                remaining_days = days_in_month - now.day
                if remaining_days > 0:
                    summary["daily_budget"] = round(remaining / remaining_days, 2)

        return summary

    def get_monthly_report(self):
        expenses = self.load_expenses()
        monthly = {}

        if not expenses:
            return {"message": "No expenses to report."}

        for exp in expenses:
            key = exp.date[:7]
            monthly.setdefault(key, []).append(exp)

        report = {}
        for month, records in monthly.items():
            data = {"total": 0, "categories": {}, "transactions": len(records)}
            for r in records:
                data["total"] += r.amount
                data["categories"].setdefault(r.category, 0)
                data["categories"][r.category] += r.amount
            report[month] = data

        return report

    def set_budget(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return {"status": "error", "error": "Budget must be greater than 0"}
            with open(self.budget_file_path, 'w', encoding='utf-8') as f:
                f.write(str(amount))
            return {"status": "success", "message": f"Budget set to Rs.{amount:.2f}"}
        except ValueError:
            return {"status": "error", "error": "Invalid budget amount"}

    def get_budget(self):
        if os.path.exists(self.budget_file_path):
            try:
                with open(self.budget_file_path, 'r', encoding='utf-8') as f:
                    return float(f.read().strip())
            except:
                return 0
        return 0

    def get_categories(self):
        return self.categories

    def add_category(self, category_name):
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            self.save_categories()
            return {"status": "success", "message": f"Category '{category_name}' added successfully!"}
        else:
            return {"status": "error", "error": "Invalid or duplicate category"}

    def reset_categories(self):
        self.categories = self.default_categories.copy()
        self.save_categories()
        return {"message": "Categories reset to default."}
