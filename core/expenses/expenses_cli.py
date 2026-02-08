from core.exceptions import (FileError, IndexError, YAMLFileNotFoundError)
from core.utils import CheckInput
from typing import Optional

class ExpensesCLI:
    def __init__(self, SetExpenses, ShowExpenses, AddExpenses,
                 EditExpenses, DeleteExpenses, ExpensesKeyExtractor):
        self.set_expenses = SetExpenses
        self.show_expenses = ShowExpenses
        self.add_expenses = AddExpenses
        self.edit_expenses = EditExpenses
        self.delete_expenses = DeleteExpenses
        self.expenses_keys = ExpensesKeyExtractor
        self.monthly_expenses_headers = []
        self.monthly_expenses_keys = []
        self.monthly_expenses_length = 0
        
    def load_keys(self) -> None:
        self.monthly_expenses_headers = self.expenses_keys.get_category_keys()
        self.monthly_expenses_keys = self.expenses_keys.get_expenses_keys()
        self.monthly_expenses_length = len(self.monthly_expenses_keys)
        
    #helper to input and validate inputted index
    def prompt_index(self, message: str, min_value: int, max_value: int) -> int:
        while True:
            try:
                index = input(message)
                if CheckInput.check_digit(index, min_value, max_value):
                    return int(index)
            except IndexError as e:
                print(e)

    #helper
    def prompt_name(self, message: str) -> str:
        name = input(message)
        return name
    
    #helper
    def prompt_value(self, message: str) -> int:
        while True:
            value = input(message)
            if value.isdigit():
                return int(value)
            print("Inputted value must be in digit!")
    
    #helper to show expenses list with index on the category
    def show_indexed_expenses_category(self, expenses_data: dict[str, dict[str, int]]) -> None:
        for index, (category, expenses) in enumerate(expenses_data.items()):
                print(f"{index + 1}. {category.upper()}")
                for expense in expenses:
                    print(f"    {expense}: {expenses[expense]}")
    
    #helper to show expenses list with index on them
    def show_indexed_expenses(self, expenses_data: dict[str, dict[str, int]]) -> None:
        index = 1
        for category, expenses in expenses_data.items():
            print(f"{category.upper()}")
            for expense in expenses:
                print(f"{index}. {expense}: {expenses[expense]}")
                index += 1
    
    #from here to below are the main methods
    def show_monthly_expenses(self) -> None:
        print(self.show_expenses.get_all_expenses())
    
    def update_monthly_expenses(self) -> None:
        try:
            self.load_keys()
        except FileError as e:
            print(e)
            return
        monthly_expenses = self.set_expenses.get_all_expenses(format_data=False)
        print("Update all expenses:\n"
              f"- Total expenses to update: {self.monthly_expenses_length}\n"
              "- you can type 's' to skip and use the original")
        for category, expenses in monthly_expenses.items():
            print(f"\n----- {category.upper()} -----")
            for expense in expenses:
                while True:
                    print(f"Set expense for {expense}")
                    new_expense = input("Enter amount ('s' to skip): ")
                    if self.set_expenses.validate_value(new_expense):
                        try:
                            self.set_expenses.update_expenses(category, expense, int(new_expense))
                        except YAMLFileNotFoundError as e:
                            print(e)
                            return
                        break
                    #use original value if user input 's'
                    elif new_expense.lower() == "s":
                        break
                    else:
                        print("inputted expense must be digit!")
        print("\n----- Expenses update completed successfully! -----\n")
        
    def add_monthly_expenses(self) -> None:
        print("")
        try:
            self.load_keys()
        except FileError as e:
            print(e)
            return
        for index, category in enumerate(self.monthly_expenses_headers):
            print(f"{index + 1}. {category}")
            if index + 1 == len(self.monthly_expenses_headers):
                print(f"{index + 2}. Add new category")
        category_index = self.prompt_index("Select category or add new one (by index): ", 1, len(self.monthly_expenses_headers) + 1)
        #input name for the new expense category and new expense
        if category_index == len(self.monthly_expenses_headers) + 1:
            new_category_name = self.prompt_name("Enter name for the new category: ")
            self.add_expenses.add_new_category_and_expense(new_category_name,
                                                           self.prompt_name("Enter name for the new expense: "),
                                                           self.prompt_value("Enter value for the new expense: "))
        else:
            self.add_expenses.add_new_expense(self.monthly_expenses_headers[category_index - 1],
                                              self.prompt_name("Enter name for the new expense: "),
                                              self.prompt_value("Enter value for the new expense: "))
        print("New expense added successfully!\n")
        
    def edit_monthly_expenses(self) -> None:
        print("")
        try:
            self.load_keys()
            expenses_data = self.edit_expenses.get_all_expenses(format_data=False)
        except FileError as e:
            print(e)
            return
        self.show_indexed_expenses(expenses_data)
        index = self.prompt_index("Select which expense to edit (by index): ", 1, len(self.monthly_expenses_keys))
        try:
            category_key, expense_key = self.edit_expenses.get_keys_by_index(expenses_data, index)
        except IndexError as e:
            print(e)
            return
        print(f"\nChoose an action for expense ({expense_key})\n"
              "1. Edit expense name\n"
              "2. Edit expense value\n"
              "3. Edit expense name and value")
        decision = self.prompt_index("Decision (by index): ", 1, 3)
        if decision in (1, 3):
            new_expense_key = self.prompt_name(f"Enter new name for ({expense_key}): ")
            self.edit_expenses.edit_expense_name(category_key, expense_key, new_expense_key)
            expense_key = new_expense_key if decision == 3 else expense_key
        if decision in (2, 3):
            new_expense_value = self.prompt_value(f"Enter new value for ({expense_key}): ")
            self.edit_expenses.edit_expense_value(category_key, expense_key, new_expense_value)
        print(f"({expense_key}) expense edited successfully!\n")
        
    def delete_monthly_expenses(self) -> None:
        print("")
        try:
            self.load_keys()
            expenses_data = self.delete_expenses.get_all_expenses(format_data=False)
        except FileError as e:
            print(e)
            return
        print("1. Delete a single expense\n"
              "2. Delete expenses by category")
        decision = self.prompt_index("Decision (by index): ", 1, 2)
        category_index: Optional[int] = None
        expense_index: Optional[int] = None
        print("")
        if decision == 1:
            self.show_indexed_expenses(expenses_data)
            #get category name based on expense_index using helper method from logic
            expense_index = self.prompt_index("Select which expense to delete (by index): ", 1, self.monthly_expenses_length)
            try:
                self.delete_expenses.delete_expense(expense_index)
            except IndexError as e:
                print(e)
                return
            print(f"expense {self.monthly_expenses_keys[expense_index - 1]} deleted successfully!\n")
        elif decision == 2:
            self.show_indexed_expenses_category(expenses_data)
            category_index = self.prompt_index("Select which category to delete (by index): ", 1, len(self.monthly_expenses_headers))
            self.delete_expenses.delete_category(self.monthly_expenses_headers[category_index - 1])
            print(f"Category {self.monthly_expenses_headers[category_index - 1]} deleted successfully!\n")