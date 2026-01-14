from core.utils import DataIO
from core.exceptions import IncorrectInputExpenses

class ExpensesLogic:
    def __init__(self):
        self.MONTHLY_EXPENSES_FILEPATH = "data/expenses_config.yaml"
        self.yaml_handler = DataIO(self.MONTHLY_EXPENSES_FILEPATH)
        self.monthly_expenses = {"necessary":{
                            "meal": 0,
                            "electricity": 0,
                            "parents": 0,
                            "fuel": 0,
                            "installment": 0,
                            "internet": 0
                        },
                            "savings":{
                            "reksa_dana": 0,
                            "gold": 0
                            },
                            "free_to_spend":{
                            "subscription": 0,
                            "left": 0
                            }}
        
    def check_inputted_values(self, value: str) -> bool:
        if value.isdigit():
            return True
        raise IncorrectInputExpenses("inputted expense must be digit!")
            
class SetExpenses(ExpensesLogic):
    def update_expenses(self, header: str, key: str, value: int):
        for i in range(10):
            self.monthly_expenses[header][key] = value
        self.yaml_handler.save_config(self.monthly_expenses)