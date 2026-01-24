from core.utils import DataIO
from pathlib import Path
from core.exceptions import IncorrectInputExpenses

class ExpensesLogic:
    def __init__(self):
        self.MONTHLY_EXPENSES_FILEPATH = Path("data/monthly_expenses.yaml")
        self.yaml_handler = DataIO.create_dataio(self.MONTHLY_EXPENSES_FILEPATH)
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
                            }}
        
    
        
    def check_input_values(self, value: str) -> bool:
        if value.isdigit():
            return True
        raise IncorrectInputExpenses("inputted expense must be digit!")
    
    def get_all_expenses(self) -> dict[str, dict[str, int | None]]:
        return self.yaml_handler.read(format_data=True)
    
class ShowExpenses(ExpensesLogic):
    pass
            
class SetExpenses(ExpensesLogic):
    def __init__(self):
        super().__init__()
        self.input_progress = 0
        self.input_header_progress = 0
        self.needs_reinput = False
    
    def reset_input_progress(self):
        self.input_progress = 0
        self.input_header_progress = 0
        self.needs_reinput = False
    
    def update_input_progress(self):
        self.input_progress += 1
        self.input_header_progress += 1 if self.input_progress in (0, 6, 8) else 0
        
    def update_not_complete(self) -> bool:
        if self.input_progress != 9:
            return True
        return False
    
    def reinput_value(self):
        self.needs_reinput = True
    
    def current_header_progress(self) -> bool:
        if self.input_progress in (0, 6, 8) and not self.needs_reinput:
            return True
        return False
    
    def update_expenses(self, header: str, key: str, value: int):
        self.monthly_expenses[header][key] = value
        self.needs_reinput = False
        if self.input_progress == 8:
            self.yaml_handler.save(self.monthly_expenses)