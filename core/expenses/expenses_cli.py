from core.expenses.expenses_logic import (SetExpenses, ShowExpenses, EditExpenses)
from core.exceptions import (YAMLFileNotFoundError, InvalidInputIndexError)
from core.utils import CheckInput

class ExpensesCLI:
    def __init__(self):
        self.set_expenses = SetExpenses()
        self.show_expenses = ShowExpenses()
        self.edit_expenses = EditExpenses()
        self.monthly_expenses_headers = ["necessary", "savings", "free_to_spend"]
        self.monthly_expenses_keys = ["meal", "electricity", "parents", "fuel", "installment",
                                      "internet", "reksa_dana", "gold", "subscription"]
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
        print("")
        for header_index, header in enumerate(self.monthly_expenses_headers):
            print(f"----- {header} -----")
            for key_index, key in enumerate(self.monthly_expenses_keys):
                if header_index == 0 and key_index > 5:
                    continue
                if header_index == 1 and (key_index < 6 or key_index >= 8):
                    continue
                if header_index == 2 and key_index != 8:
                    continue
                print(f"{key_index + 1}. {key}")
        print("")
        index = self.prompt_index("Select which expense to edit (by index): ", 1, len(self.monthly_expenses_keys))
        index -= 1
        while True:
            new_expense = input(f"Enter new expense for ({self.monthly_expenses_keys[index]}): ")
            if new_expense.isdigit():
                break
            print("Expense must be in digit!")
        self.edit_expenses.update_edit_expense(index, new_expense)
        print(f"({self.monthly_expenses_keys[index]}) expense edited successfully!\n")