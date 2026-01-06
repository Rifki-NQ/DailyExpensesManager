from core.salary import SalaryCLI
from core.utils import CheckInput, DataIO

class MainMenu:
    def __init__(self, total_menu, total_sub_menu):
        self.total_menu = total_menu
        self.total_sub_menu = total_sub_menu
        self.is_running = True
        self.choosen_menu = 0
        self.choosen_sub_menu = 0
        self.salary_data = SalaryCLI()
    
    def show_menu(self):
        print("Daily Expenses Manager")
        print("< ------------------ >")
        print("1. Salary DATA")
    
    def show_sub_menu(self):
        print("< ------------------ >")
        if self.choosen_menu == 1:
            print("1. Show current salary simulation")
            print("2. Change curerent salary simulation")
    
    def input_menu_choices(self):
        while self.is_running:
            self.choosen_menu = input("Input by index (q to quit): ")
            if CheckInput.check_digit(self.choosen_menu, 1, self.total_menu):
                self.choosen_menu = int(self.choosen_menu)
                break
            elif self.choosen_menu.lower() == "q":
                self.is_running = False
                
    def input_sub_menu_choices(self):
        while self.is_running:
            self.choosen_sub_menu = input("Input by index (q to quit): ")
            if CheckInput.check_digit(self.choosen_sub_menu, 1, self.total_sub_menu):
                self.choosen_sub_menu = int(self.choosen_sub_menu)
                break
            elif self.choosen_sub_menu.lower() == "q":
                self.is_running = False
                
    def run_choosen_method(self):
        #Salary menu
        if self.choosen_menu == 1:
            if self.choosen_sub_menu == 1:
                self.salary_data.show_current_simulation()
            elif self.choosen_sub_menu == 2:
                self.salary_data.change_current_simulation()
    
    def run(self):
        while self.is_running:
            self.show_menu()
            self.input_menu_choices()
            self.show_sub_menu()
            self.input_sub_menu_choices()
            self.run_choosen_method()
    
if __name__ == "__main__":
    app = MainMenu(1, 2)
    app.run()