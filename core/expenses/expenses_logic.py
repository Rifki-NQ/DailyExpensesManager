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
        
    def validate_value(self, value: str) -> bool:
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
        keys = []
        for category, expenses in expenses_data.items():
            for expense in expenses:
                if count == index:
                    keys.append(category)
                    keys.append(expense)
                count+=1
        if returned_key == "category":
            return keys[0]
        elif returned_key == "expenses":
            return keys[1]
    
class ShowExpenses(ExpensesLogic):
    pass
            
class UpdateExpenses(ExpensesLogic):    
    def update_expenses(self, category_key: str, expenses_key: str, new_expense: int) -> None:
        monthly_expenses = self.yaml_handler.read()
        monthly_expenses[category_key][expenses_key] = new_expense
        self.yaml_handler.save(monthly_expenses)
        
class AddExpenses(ExpensesLogic):
    def add_new_expense(self, category_name: str, new_expense_name: str, new_expense_value: int) -> None:
        monthly_expenses = self.yaml_handler.read()
        monthly_expenses[category_name][new_expense_name] = new_expense_value
        self.yaml_handler.save(monthly_expenses)
    
    def add_new_category_and_expense(self, new_category_name: str, new_expense_name: str, new_expense_value: int) -> None:
        monthly_expenses = self.yaml_handler.read()
        monthly_expenses[new_category_name] = {new_expense_name: new_expense_value}
        self.yaml_handler.save(monthly_expenses)
            
class EditExpenses(ExpensesLogic):
    def update_edit_expense(self, category_key: str, expenses_key: str, new_expense: int) -> None:
        #read the original data first, modify it then save it back
        expenses_data = self.yaml_handler.read()
        expenses_data[category_key][expenses_key] = new_expense
        self.yaml_handler.save(expenses_data)