from core.exceptions import (InvalidDaysLengthError, FileError)
from typing import Literal

class DailyExpensesCLI():
    def __init__(self, salary_logic, expenses_logic, simulation_logic):
        self.salary_data = salary_logic
        self.expenses_data = expenses_logic
        self.daily_expenses = simulation_logic
        self.total_salary: int
        self.salary_date: str
        self.total_expenses: int
    
    def get_salary(self, include: Literal["date", "salary"]) -> str | int:
        salary_data = self.salary_data.load_salary_simulation()
        if include == "date":
            return salary_data[0]
        elif include == "salary":
            return salary_data[1]
    
    def get_expenses(self, merge: bool = True) -> int:
        all_expenses = self.expenses_data.get_all_expenses()
        return all_expenses
    
    def load_total_data(self) -> None:
        self.salary_date = self.get_salary("date")
        self.total_salary = self.get_salary("salary")
        self.total_expenses = self.get_expenses()
    
    def prompt_days_length(self) -> int:
        while True:
            try:
                days_length = input("Enter days length (1 to 31): ")
                if self.daily_expenses.validate_days_length(days_length):
                    return int(days_length)
            except InvalidDaysLengthError as e:
                print(e)
    
    def prompt_option(self) -> bool:
        while True:
            option = input("y/n: ")
            if option.lower() == "y":
                return True
            elif option.lower() == "n":
                return False
            print("Invalid option inputted! (y = yes, n = no)")

    def show_daily_expenses(self):
        try:
            self.load_total_data()
        except FileError as e:
            print(e)
            return
        print("This simulation is based on data with:\n"
              f"- total salary: {self.total_salary}\n"
              f"- date of the salary: {self.salary_date}\n"
              f"- total monthly expenses: {self.total_expenses}")
        print("Use custom days length? ")
        custom_length_option = self.prompt_option()
        if custom_length_option:
            days_length = self.prompt_days_length()