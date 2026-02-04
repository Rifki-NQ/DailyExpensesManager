from core.salary.salary_cli import SalaryCLI
from core.salary.salary_logic import (SalaryLogic, CurrentSalarySimulation, ChangeSalarySimulation,
                                      AddNewSalary, EditSalary, DeleteSalary)
from core.expenses.expenses_cli import ExpensesCLI
from core.expenses.expenses_logic import (ExpensesLogic, UpdateExpenses, ExpensesKeyExtractor,
                                          ShowExpenses, AddExpenses, EditExpenses)
from core.simulation.simulation_cli import DailyExpensesCLI
from core.simulation.simulation_logic import DailyExpensesLogic
from core.utils import DataIO, CheckInput
from core.exceptions import AppError, InvalidInputIndexError
from pathlib import Path

class MainMenu:
    def __init__(self, total_menu, total_sub_menu_first, total_sub_menu_second):
        self.total_menu = total_menu
        self.total_sub_menu_first = total_sub_menu_first
        self.total_sub_menu_second = total_sub_menu_second
        self.is_running = True
        self.choosen_menu = 0
        self.choosen_sub_menu = 0
        self.SALARY_DATA_FILEPATH = "data/salary_data.csv"
        self.CONFIG_FILEPATH = "data/config.yaml"
        self.MONTHLY_EXPENSES_FILEPATH = "data/monthly_expenses.yaml"
        self.salary_file_handler = DataIO.create_dataio(Path(self.SALARY_DATA_FILEPATH))
        self.config_file_handler = DataIO.create_dataio(Path(self.CONFIG_FILEPATH))
        self.monthly_expenses_file_handler = DataIO.create_dataio(Path(self.MONTHLY_EXPENSES_FILEPATH))
        self.salary_data = SalaryCLI(SalaryLogic(self.salary_file_handler, self.config_file_handler),
                                     CurrentSalarySimulation(self.salary_file_handler, self.config_file_handler),
                                     ChangeSalarySimulation(self.salary_file_handler, self.config_file_handler),
                                     AddNewSalary(self.salary_file_handler, self.config_file_handler),
                                     EditSalary(self.salary_file_handler, self.config_file_handler),
                                     DeleteSalary(self.salary_file_handler, self.config_file_handler))
        self.expenses_data = ExpensesCLI(UpdateExpenses(self.monthly_expenses_file_handler),
                                         ShowExpenses(self.monthly_expenses_file_handler),
                                         AddExpenses(self.monthly_expenses_file_handler),
                                         EditExpenses(self.monthly_expenses_file_handler),
                                         ExpensesKeyExtractor(self.monthly_expenses_file_handler))
        self.simulation_logic = DailyExpensesLogic(CurrentSalarySimulation(self.salary_file_handler, self.config_file_handler),
                                                   ExpensesLogic(self.monthly_expenses_file_handler))
        self.daily_expenses = DailyExpensesCLI(self.simulation_logic)
    
    def show_menu(self):
        print("Daily Expenses Manager")
        print("< ------------------ >")
        print("1. Show daily expenses simulation")
        print("2. Salary Management")
        print("3. Expenses Management")
    
    def show_sub_menu(self):
        print("< ------------------ >")
        if self.choosen_menu == 2:
            print("1. Show current salary simulation")
            print("2. Change current salary simulation")
            print("3. Add new salary")
            print("4. Edit salary")
            print("5. Delete salary")
        elif self.choosen_menu == 3:
            print("1. Show monthly expenses")
            print("2. Update all monthly expenses")
            print("3. Add new monthly expense")
            print("4. Edit monthly expense")
    
    def input_menu_choices(self):
        while self.is_running:
            try:
                self.choosen_menu = input("Input by index (q to quit): ")
                if CheckInput.check_digit(self.choosen_menu, 1, self.total_menu, quit_option=True):
                    self.choosen_menu = int(self.choosen_menu)
                    break
                elif self.choosen_menu.lower() == "q":
                    self.is_running = False
            except InvalidInputIndexError as e:
                print(e)
                
    def input_sub_menu_choices(self):
        while self.is_running:
            if self.choosen_menu == 1:
                break
            if self.choosen_menu == 2:
                try:
                    self.choosen_sub_menu = input("Input by index (q to quit): ")
                    if CheckInput.check_digit(self.choosen_sub_menu, 1, self.total_sub_menu_first, quit_option=True):
                        self.choosen_sub_menu = int(self.choosen_sub_menu)
                        break
                    elif self.choosen_sub_menu.lower() == "q":
                        break
                except InvalidInputIndexError as e:
                    print(e)
            elif self.choosen_menu == 3:
                try:
                    self.choosen_sub_menu = input("Input by index (q to quit): ")
                    if CheckInput.check_digit(self.choosen_sub_menu, 1, self.total_sub_menu_second, quit_option=True):
                        self.choosen_sub_menu = int(self.choosen_sub_menu)
                        break
                    elif self.choosen_sub_menu.lower() == "q":
                        break
                except InvalidInputIndexError as e:
                    print(e)
                
    def run_choosen_method(self):
        #Main feature
        if self.choosen_menu == 1:
            self.daily_expenses.show_daily_expenses()
        #Salary menu
        if self.choosen_menu == 2:
            if self.choosen_sub_menu == 1:
                self.salary_data.show_current_simulation()
            elif self.choosen_sub_menu == 2:
                self.salary_data.change_current_simulation()
            elif self.choosen_sub_menu == 3:
                self.salary_data.add_new_salary()
            elif self.choosen_sub_menu == 4:
                self.salary_data.edit_salary()
            elif self.choosen_sub_menu == 5:
                self.salary_data.delete_salary()
        #Expenses menu
        if self.choosen_menu == 3:
            if self.choosen_sub_menu == 1:
                self.expenses_data.show_monthly_expenses()
            elif self.choosen_sub_menu == 2:
                self.expenses_data.update_monthly_expenses()
            elif self.choosen_sub_menu == 3:
                self.expenses_data.add_monthly_expenses()
            elif self.choosen_sub_menu == 4:
                self.expenses_data.edit_monthly_expenses()
    
    def run(self):
        while self.is_running:
            try:
                self.show_menu()
                self.input_menu_choices()
                self.show_sub_menu()
                self.input_sub_menu_choices()
                self.run_choosen_method()
            except AppError as e:
                print(e)
    
if __name__ == "__main__":
    app = MainMenu(3, 5, 3)
    app.run()