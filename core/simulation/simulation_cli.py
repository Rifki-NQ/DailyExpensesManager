from core.exceptions import (InvalidDaysLengthError, FileError)
from typing import Optional

class DailyExpensesCLI():
    def __init__(self, simulation_logic):
        self.simulation_logic = simulation_logic
        self.total_salary: Optional[int] = None
        self.salary_date: Optional[str] = None
        self.total_expenses: Optional[int] = None
    
    def load_total_data(self) -> None:
        self.salary_date = self.simulation_logic.get_salary("date")
        self.total_salary = self.simulation_logic.get_salary("salary")
        self.total_expenses = self.simulation_logic.get_expenses()
    
    def prompt_days_length(self) -> int:
        minimum_days_length, maximum_days_length = self.simulation_logic.get_valid_days_length()
        while True:
            try:
                days_length = input(f"Enter days length ({minimum_days_length} to {maximum_days_length}): ")
                if self.simulation_logic.validate_days_length(days_length):
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
            all_expenses = self.simulation_logic.get_expenses(merge=False)
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
        else:
            days_length = 30
        dict_daily_expenses = self.simulation_logic.process_daily_expenses(days_length, all_expenses)
        print("Here")