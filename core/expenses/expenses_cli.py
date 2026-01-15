from core.expenses.expenses_logic import (SetExpenses)
from core.exceptions import (IncorrectInputExpenses, ConfigFileNotFoundError)

class ExpensesCLI:
    def __init__(self):
        self.set_expenses = SetExpenses()
        self.monthly_expenses_headers = ["necessary", "savings", "free_to_spend"]
        self.monthly_expenses_keys = ["meal", "electricity", "parents", "fuel", "installment",
                                      "internet", "reksa_dana", "gold", "subscription"]
    
    def set_monthly_expenses(self):
        self.set_expenses.reset_input_progress()
        while self.set_expenses.update_not_complete():
            if self.set_expenses.current_header_progress():
                    print(f"-----{self.monthly_expenses_headers[self.set_expenses.input_header_progress].upper()}-----")
            try:
                new_expense = input(f"Set expense for {self.monthly_expenses_keys[self.set_expenses.input_progress]}: ")
                if self.set_expenses.check_input_values(new_expense):
                    self.set_expenses.update_expenses(self.monthly_expenses_headers[self.set_expenses.input_header_progress],
                                                      self.monthly_expenses_keys[self.set_expenses.input_progress], int(new_expense))
                    self.set_expenses.update_input_progress()
            except IncorrectInputExpenses as e:
                print(e)
            except ConfigFileNotFoundError as e:
                print(e)
                return