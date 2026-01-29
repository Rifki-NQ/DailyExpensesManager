from core.exceptions import (InvalidDaysLengthError, FileError)

class DailyExpensesCLI():
    def __init__(self, simulation_logic):
        self.simulation_logic = simulation_logic
        self.total_salary: int
        self.salary_date: str
        self.total_expenses: int
    
    def load_total_data(self) -> None:
        self.salary_date = self.simulation_logic.get_salary("date")
        self.total_salary = self.simulation_logic.get_salary("salary")
        self.total_expenses = self.simulation_logic.get_expenses()
    
    def prompt_days_length(self) -> int:
        while True:
            try:
                days_length = input("Enter days length (1 to 31): ")
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