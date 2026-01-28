from core.exceptions import (InvalidDaysLengthError)

class DailyExpensesCLI():
    def __init__(self, salary_logic, expenses_logic, simulation_logic):
        self.salary_data = salary_logic
        self.expenses_data = expenses_logic
        self.daily_expenses = simulation_logic
        self.total_salary = 0
        self.total_expenses = 0
    
    def get_salary(self) -> int:
        pass
    
    def get_expenses(self, merge: False) -> int:
        pass
    
    def load_total_data(self, salary, expenses) -> None:
        pass
    
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
        print("This simulation is based on data with:\n"
              f"- total salary: \n"
              f"- date of the salary: \n"
              f"- total monthly expenses: ")
        print("Use custom days length? ")
        custom_length_option = self.prompt_option()
        if custom_length_option:
            days_length = self.prompt_days_length()