from core.exceptions import (InvalidDaysLengthError)
from typing import Literal

class DailyExpensesLogic():
    def __init__(self, salary_logic, expenses_logic):
        self.salary_data = salary_logic
        self.expenses_data = expenses_logic
        self.MINIMUM_DAYS_LENGTH = 1
        self.MAXIMUM_DAYS_LENGTH = 31
    
    def validate_days_length(self, value: str) -> bool:
        if value.isdigit() and int(value) < self.MINIMUM_DAYS_LENGTH:
            raise InvalidDaysLengthError(f"Days length cannot below {self.MINIMUM_DAYS_LENGTH}!")
        elif value.isdigit() and int(value) > self.MAXIMUM_DAYS_LENGTH:
            raise InvalidDaysLengthError(f"Days length cannot be over {self.MAXIMUM_DAYS_LENGTH} days!")
        elif value.isdigit():
            return True
        else:
            raise InvalidDaysLengthError("Days length must be in digit!")
        
    def get_valid_days_length(self) -> tuple[int, int]:
        return self.MINIMUM_DAYS_LENGTH, self.MAXIMUM_DAYS_LENGTH
        
    def get_salary(self, include: Literal["date", "salary"]) -> str | int:
        salary_data = self.salary_data.load_salary_simulation()
        if include == "date":
            return salary_data[0]
        elif include == "salary":
            return salary_data[1]
    
    def get_expenses(self, merge: bool = True) -> int | dict[str, dict[str, int]]:
        if merge:
            return self.expenses_data.get_total_expenses()
        return self.expenses_data.get_all_expenses(format_data=False)
    
    #check if total salary is not less than total expenses
    def is_valid_data_amount(self, total_salary, total_expenses) -> bool:
        if total_salary > total_expenses:
            return True
        return False
    
    def process_daily_expenses(self, days_length: int, total_salary: int, total_expenses: int) -> int:
        expenses_left = total_salary - total_expenses
        return expenses_left // days_length