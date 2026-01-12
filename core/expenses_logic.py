from core.utils import DataIO

class ExpensesLogic:
    def __init__(self):
        self.MONTHLY_EXPENSES_FILEPATH = "data/expenses_config.yaml"
        self.yaml_handler = DataIO(self.MONTHLY_EXPENSES_FILEPATH)
        
    def check_monthly_expenses(self):
        expenses = self.yaml_handler.read_config()