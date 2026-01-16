from core.salary.salary_cli import SalaryCLI
from core.expenses.expenses_cli import ExpensesCLI
from core.utils import CheckInput
from core.exceptions import AppError, InvalidInputIndexError

class MainMenu:
    def __init__(self, total_menu, total_sub_menu_first, total_sub_menu_second):
        self.total_menu = total_menu
        self.total_sub_menu_first = total_sub_menu_first
        self.total_sub_menu_second = total_sub_menu_second
        self.is_running = True
        self.choosen_menu = 0
        self.choosen_sub_menu = 0
        self.salary_data = SalaryCLI()
        self.expenses_data = ExpensesCLI()
    
    def show_menu(self):
        print("Daily Expenses Manager")
        print("< ------------------ >")
        print("1. Salary DATA")
        print("2. Expenses DATA")
    
    def show_sub_menu(self):
        print("< ------------------ >")
        if self.choosen_menu == 1:
            print("1. Show current salary simulation")
            print("2. Change current salary simulation")
            print("3. Add new salary")
        elif self.choosen_menu == 2:
            print("1. Set monthly expenses")
    
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
        if self.choosen_menu == 1:
            try:
                self.choosen_sub_menu = input("Input by index (q to quit): ")
                if CheckInput.check_digit(self.choosen_sub_menu, 1, self.total_sub_menu_first, quit_option=True):
                    self.choosen_sub_menu = int(self.choosen_sub_menu)
                    return
                elif self.choosen_sub_menu.lower() == "q":
                    return
            except InvalidInputIndexError as e:
                print(e)
        elif self.choosen_menu == 2:
            try:
                self.choosen_sub_menu = input("Input by index (q to quit): ")
                if CheckInput.check_digit(self.choosen_sub_menu, 1, self.total_sub_menu_second, quit_option=True):
                    self.choosen_sub_menu = int(self.choosen_sub_menu)
                    return
                elif self.choosen_sub_menu.lower() == "q":
                    return
            except InvalidInputIndexError as e:
                print(e)
                
    def run_choosen_method(self):
        #Salary menu
        if self.choosen_menu == 1:
            if self.choosen_sub_menu == 1:
                self.salary_data.show_current_simulation()
            elif self.choosen_sub_menu == 2:
                self.salary_data.change_current_simulation()
            elif self.choosen_sub_menu == 3:
                self.salary_data.add_new_salary()
        #Expenses menu
        if self.choosen_menu == 2:
            if self.choosen_sub_menu == 1:
                self.expenses_data.set_monthly_expenses()
    
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
    app = MainMenu(2, 3, 1)
    app.run()