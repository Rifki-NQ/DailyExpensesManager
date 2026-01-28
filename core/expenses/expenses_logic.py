from core.utils import DataIO
from pathlib import Path

class ExpensesLogic:
    def __init__(self):
        self.MONTHLY_EXPENSES_FILEPATH = "data/monthly_expenses.yaml"
        self.yaml_handler = DataIO.create_dataio(Path(self.MONTHLY_EXPENSES_FILEPATH))
        self.monthly_expenses_headers = ["necessary", "savings", "free_to_spend"]
        self.monthly_expenses_keys = ["meal", "electricity", "parents", "fuel", "installment",
                                      "internet", "reksa_dana", "gold", "subscription"]
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
                            "subscription": 0
                            }}
        
    def check_input_values(self, value: str) -> bool:
        if value.isdigit():
            return True
        return False
    
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
    
    def reset_input_progress(self) -> None:
        self.input_progress = 0
        self.input_header_progress = 0
        self.needs_reinput = False
    
    def update_input_progress(self) -> None:
        self.input_progress += 1
        self.input_header_progress += 1 if self.input_progress in (0, 6, 8) else 0
        
    def update_not_complete(self) -> bool:
        if self.input_progress != 9:
            return True
        return False
    
    def reinput_value(self) -> None:
        self.needs_reinput = True
    
    def skip_input(self, header: str, key: str) -> None:
        self.original_expenses = self.yaml_handler.read()
        original_value = self.original_expenses[header][key]
        self.update_expenses(header, key, original_value)
    
    def current_header_progress(self) -> bool:
        if self.input_progress in (0, 6, 8) and not self.needs_reinput:
            return True
        return False
    
    def update_expenses(self, header: str, key: str, value: int) -> None:
        self.monthly_expenses[header][key] = value
        self.needs_reinput = False
        if self.input_progress == 8:
            self.yaml_handler.save(self.monthly_expenses)
            
class EditExpenses(ExpensesLogic):
    def update_edit_expense(self, index: int, new_expense: int) -> None:
        if index < 6:
            header = self.monthly_expenses_headers[0]
        if index in range(6, 8):
            header = self.monthly_expenses_headers[1]
        if index == 8:
            header = self.monthly_expenses_headers[2]
        #read the original data first, modify it then save it back
        self.monthly_expenses = self.yaml_handler.read()
        self.monthly_expenses[header][self.monthly_expenses_keys[index]] = int(new_expense)
        self.yaml_handler.save(self.monthly_expenses)