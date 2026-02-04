from core.exceptions import (FileError, YAMLFileNotFoundError, InvalidInputIndexError)
from core.utils import CheckInput

class ExpensesCLI:
    def __init__(self, SetExpenses, ShowExpenses, AddExpenses, EditExpenses, ExpensesKeyExtractor):
        self.set_expenses = SetExpenses
        self.show_expenses = ShowExpenses
        self.add_expenses = AddExpenses
        self.edit_expenses = EditExpenses
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
            except InvalidInputIndexError as e:
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
        try:
            self.load_keys()
            expenses_data = self.edit_expenses.get_all_expenses(format_data=False)
        except FileError as e:
            print(e)
            return
        print("")
        index = 1
        for category in expenses_data:
            print(f"----- {category.upper()} -----")
            for expense in expenses_data[category]:
                print(f"{index}. {expense}")
                index += 1
        print("")
        index = self.prompt_index("Select which expense to edit (by index): ", 1, len(self.monthly_expenses_keys))
        index -= 1
        while True:
            new_expense = input(f"Enter new expense for ({self.monthly_expenses_keys[index]}): ")
            if new_expense.isdigit():
                break
            print("Expense must be in digit!")
        self.edit_expenses.update_edit_expense(self.edit_expenses.get_expenses_by_index(expenses_data, index, "category"),
                                               self.edit_expenses.get_expenses_by_index(expenses_data, index, "expenses"),
                                               int(new_expense))
        print(f"({self.monthly_expenses_keys[index]}) expense edited successfully!\n")