from core.exceptions import (InvalidDaysLengthError)
from typing import Literal

class DailyExpensesLogic():
    def __init__(self, salary_logic, expenses_logic):
        self.salary_data = salary_logic
        self.expenses_data = expenses_logic
    
    def validate_days_length(self, value: str) -> bool:
        if value.isdigit() and int(value) < 1:
            raise InvalidDaysLengthError("Days length cannot below 1!")
        elif value.isdigit() and int(value) > 31:
            raise InvalidDaysLengthError("Days length cannot be over 31 days!")
        elif value.isdigit():
            return True
        else:
            raise InvalidDaysLengthError("Days length must be in digit!")
        
    def get_salary(self, include: Literal["date", "salary"]) -> str | int:
        salary_data = self.salary_data.load_salary_simulation()
        if include == "date":
            return salary_data[0]
        elif include == "salary":
            return salary_data[1]
    
    def get_expenses(self, merge: bool = True) -> int:
        all_expenses = self.expenses_data.get_total_expenses()
        return all_expenses