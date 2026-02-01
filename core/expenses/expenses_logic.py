from typing import Literal
ExpensesMergeOptions = Literal["necessary", "savings", "free_to_spend"]
KeysOption = Literal["category", "expenses"]

class ExpensesKeyExtractor:
    def __init__(self, YAMLFileHandler):
        self.yaml_handler = YAMLFileHandler
        
    def get_category_keys(self) -> list[str]:
        expenses_data = self.yaml_handler.read()
        category_keys = []
        for category_key in expenses_data.keys():
            category_keys.append(category_key)
        return category_keys
    
    def get_expenses_keys(self) -> list[str]:
        expenses_data = self.yaml_handler.read()
        expenses_keys = []
        for category_key in expenses_data:
            for expenses_key in expenses_data[category_key]:
                expenses_keys.append(expenses_key)
        return expenses_keys

class ExpensesLogic:
    def __init__(self, YAMLFileHandler):
        self.yaml_handler = YAMLFileHandler
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
    
    def get_all_expenses(self, format_data: bool = True) -> str | dict[str, dict[str, int]]:
        return self.yaml_handler.read(format_data=format_data)
    
    def get_total_expenses(self) -> int:
        expenses_data = self.yaml_handler.read(format_data=False)
        return self._get_merged_expenses(expenses_data, merge="all")
    
    def get_total_expenses_category(self, merge_category: ExpensesMergeOptions) -> int:
        expenses_data = self.yaml_handler.read(format_data=False)
        return self._get_merged_expenses(expenses_data, merge=merge_category)
    
    #helper for getting merged expenses
    def _get_merged_expenses(self, data: dict[str, dict[str, int]], merge: ExpensesMergeOptions) -> int:
        merged_expenses = 0
        if merge == "all":
            for inner_dict in data.values():
                for value in inner_dict.values():
                    merged_expenses += value
            return merged_expenses
        else:
            for value in data[merge].values():
                merged_expenses += value
            return merged_expenses
    
    #helper for getting expense by index (based on the 2nd level of the dict total keys)
    def get_expenses_by_index(self, expenses_data: dict, index: int, returned_key: KeysOption) -> str:
        count = 0
        for category, expenses in expenses_data.items():
            for expense in expenses:
                if count == index and returned_key == "category":
                    return category
                elif count == index and returned_key == "expenses":
                    return expense
                count+=1
    
class ShowExpenses(ExpensesLogic):
    pass
            
class SetExpenses(ExpensesLogic):
    def __init__(self, YAMLFileHandler):
        super().__init__(YAMLFileHandler)
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
        original_expenses = self.yaml_handler.read()
        original_value = original_expenses[header][key]
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
    def update_edit_expense(self, category_key: str, expenses_key: str, new_expense: int) -> None:
        #read the original data first, modify it then save it back
        expenses_data = self.yaml_handler.read()
        expenses_data[category_key][expenses_key] = new_expense
        self.yaml_handler.save(expenses_data)