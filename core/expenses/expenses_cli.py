from core.exceptions import (FileError, YAMLFileNotFoundError, InvalidInputIndexError)
from core.utils import CheckInput

class ExpensesCLI:
    def __init__(self, SetExpenses, ShowExpenses, EditExpenses, ExpensesKeyExtractor):
        self.set_expenses = SetExpenses
        self.show_expenses = ShowExpenses
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

    def show_monthly_expenses(self) -> None:
        print(self.show_expenses.get_all_expenses())
    
    def set_monthly_expenses(self) -> None:
        try:
            self.load_keys()
        except FileError as e:
            print(e)
            return
        self.set_expenses.reset_input_progress()
        while self.set_expenses.update_not_complete():
            if self.set_expenses.current_header_progress():
                    print(f"----- {self.monthly_expenses_headers[self.set_expenses.input_header_progress].upper()} -----")
            try:
                print(f"Set expense for {self.monthly_expenses_keys[self.set_expenses.input_progress]} or type 's' to skip and use the original")
                new_expense = input("Enter amount ('s' to skip): ")
                if self.set_expenses.check_input_values(new_expense):
                    self.set_expenses.update_expenses(self.monthly_expenses_headers[self.set_expenses.input_header_progress],
                                                      self.monthly_expenses_keys[self.set_expenses.input_progress], int(new_expense))
                    self.set_expenses.update_input_progress()
                #use original value if user input 's'
                elif new_expense.lower() == "s":
                    self.set_expenses.skip_input(self.monthly_expenses_headers[self.set_expenses.input_header_progress],
                                                      self.monthly_expenses_keys[self.set_expenses.input_progress])
                    self.set_expenses.update_input_progress()
                else:
                    print("inputted expense must be digit!")
                    self.set_expenses.reinput_value()
            except YAMLFileNotFoundError as e:
                print(e)
                return
        print("----- Expenses updated successfully! -----\n")
        
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