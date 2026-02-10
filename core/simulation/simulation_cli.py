from core.exceptions import (InvalidDaysLengthError, FileError)
from typing import Optional

class DailyExpensesSimulationCLI:
    def __init__(self, simulation_logic):
        self.simulation_logic = simulation_logic
        self.total_salary: Optional[int] = None
        self.salary_date: Optional[str] = None
        self.total_expenses: Optional[int] = None
    
    def load_total_data(self) -> None:
        self.salary_date = self.simulation_logic.get_salary("date")
        self.total_salary = self.simulation_logic.get_salary("salary")
        self.total_expenses = self.simulation_logic.get_expenses(merge=True)
    
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

    def show_daily_simulation(self):
        try:
            self.load_total_data()
            if not self.simulation_logic.is_valid_data_amount(self.total_salary, self.total_expenses):
                print("current simulation salary is less than current monthly expenses\n"
                      "impossible to do daily simulation!")
                return
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
        daily_free_to_spend = self.simulation_logic.process_daily_expenses(days_length,
                                                                      self.total_salary,
                                                                      self.total_expenses)
        print(f"\nYour daily free to spend is: {daily_free_to_spend} / day\n")
        
class DailyExpensesDataCLI:
    def __init__(self, daily_expenses_data_logic):
        self.logic = daily_expenses_data_logic
        
    def show_daily_expenses(self):
        print("")
        print(self.logic.get_daily_expenses(format_data = True))