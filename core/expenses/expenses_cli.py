from core.expenses.expenses_logic import (SetExpenses, ShowExpenses)
from core.exceptions import (YAMLFileNotFoundError)

class ExpensesCLI:
    def __init__(self):
        self.set_expenses = SetExpenses()
        self.show_expenses = ShowExpenses()
        self.monthly_expenses_headers = ["necessary", "savings", "free_to_spend"]
        self.monthly_expenses_keys = ["meal", "electricity", "parents", "fuel", "installment",
                                      "internet", "reksa_dana", "gold", "subscription"]
    
    def show_monthly_expenses(self) -> None:
        print(self.show_expenses.get_all_expenses())
    
    def set_monthly_expenses(self) -> None:
        self.set_expenses.reset_input_progress()
        while self.set_expenses.update_not_complete():
            if self.set_expenses.current_header_progress():
                    print(f"-----{self.monthly_expenses_headers[self.set_expenses.input_header_progress].upper()}-----")
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