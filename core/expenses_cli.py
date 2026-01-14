from core.expenses_logic import (SetExpenses)
from core.exceptions import (IncorrectInputExpenses, ConfigFileNotFoundError)

class ExpensesCLI:
    def __init__(self):
        self.set_expenses = SetExpenses()
        self.monthly_expenses_headers = ["necessary", "savings", "free_to_spend"]
        self.monthly_expenses_keys = ["meal", "electricity", "parents", "fuel", "installment",
                                      "internet", "reksa_dana", "gold", "subscription"]
    
    def set_monthly_expenses(self):
        input_progress = 0
        input_header_progress = 0
        while input_progress != 9:
            if input_progress in (0, 6, 8):
                    print(f"-----{self.monthly_expenses_headers[input_header_progress].upper()}-----")
            try:
                new_expense = input(f"Set expense for {self.monthly_expenses_keys[input_progress]}: ")
                if self.set_expenses.check_inputted_values(new_expense):
                    input_progress += 1
                    input_header_progress += 1 if input_progress in (0, 6, 8) else 0
            except IncorrectInputExpenses as e:
                print(e)
            except ConfigFileNotFoundError as e:
                print(e)
                return