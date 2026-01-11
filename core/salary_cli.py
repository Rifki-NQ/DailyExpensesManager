from core.salary_logic import (SalaryBase, CurrentSalarySimulation, ChangeSalarySimulation,
                               AddNewSalary)
from core.exceptions import (FileError, EmptyDataAppError,
                             InvalidInputIndexError, ConfigFileNotFoundError)

class SalaryCLI:
    def __init__(self):
        self.salary_utils = SalaryBase()
        self.show = CurrentSalarySimulation()
        self.change = ChangeSalarySimulation()
        self.add = AddNewSalary()
    
    def show_current_simulation(self):
        try:
            current_simulation = self.show.load_salary_simulation()
            print(current_simulation)
        except FileError as e:
            print(e)
            return
            
    def change_current_simulation(self):
        try:
            all_salary = self.salary_utils.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        while True:
            try:
                index = input("Select which simulation to load (by index): ")
                if self.change.check_inputted_index(index, 1, len(all_salary)):
                    break
            except InvalidInputIndexError as e:
                print(e)
        try:
            self.change.update_current_simulation(index)
        except ConfigFileNotFoundError as e:
            print(e)
            return
        print("Simulation changed successfully!")
        
    def add_new_salary(self):
        try:
            new_salary_date = input("Enter the date for your new salary: ")
            self.add.check_input_date(new_salary_date)
        except:
            pass