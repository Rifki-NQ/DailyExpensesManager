from core.salary.salary_logic import (SalaryBase, CurrentSalarySimulation, ChangeSalarySimulation,
                               AddNewSalary, EditSalary)
from core.exceptions import (FileError, EmptyDataAppError, DuplicatedDateError,
                             InvalidInputIndexError, YAMLFileNotFoundError,
                             IncorrectTimeFormatError, IncorrectInputSalary,
                             CSVFileNotFoundError, InvalidFileTypeError)

class SalaryCLI:
    def __init__(self):
        self.salary_utils = SalaryBase()
        self.show = CurrentSalarySimulation()
        self.change = ChangeSalarySimulation()
        self.add = AddNewSalary()
        self.edit = EditSalary()
        self.handle_duplicated_date = False
    
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
                if self.salary_utils.check_input_index(index, 1, len(all_salary)):
                    break
            except InvalidInputIndexError as e:
                print(e)
        try:
            self.change.update_current_simulation(index)
            print("Simulation changed successfully!")
        except YAMLFileNotFoundError as e:
            print(e)
        
    def add_new_salary(self):
        #input new date then validate
        self.add.reset()
        while True:
            try:
                new_date = input("Input the date for your new salary: ")
                self.add.check_input_date(new_date)
                break
            except DuplicatedDateError as e:
                print(e)
                self.handle_duplicated_date = True
                break
            except IncorrectTimeFormatError as e:
                print(e)
        #handle duplicated date of salary
        if self.handle_duplicated_date:
            print(
                "Choose an action\n"
                "1. Replace the existing salary with the new one\n"
                "2. Add the new salary to the existing salary\n"
                "3. Cancel the operation"
                )
            while True:
                try:
                    index = input("Decision (by index): ")
                    if self.salary_utils.check_input_index(index, 1, 3):
                        index = int(index)
                        break
                except InvalidInputIndexError as e:
                    print(e)
            self.add.handle_duplicate_date_salary(index)
            if self.add.exit_current_process:
                return
        #input new salary
        while True:
            try:
                new_salary = input("Input the new salary: ")
                new_salary = self.add.check_input_salary(new_salary)
                break
            except IncorrectInputSalary as e:
                print(e)
        try:
            self.add.update_new_salary(new_date, new_salary)
            print("New salary added successfully!")
        except CSVFileNotFoundError as e:
            print(e)
            
    def edit_salary(self):
        try:
            all_salary = self.salary_utils.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        while True:
            try:
                index = input("Select which salary to edit (by index): ")
                if self.salary_utils.check_input_index(index, 1, len(all_salary)):
                    index = int(index)
                    break
            except InvalidInputIndexError as e:
                print(e)
        while True:
            try:
                new_salary = input("Input the new salary: ")
                new_salary = self.edit.check_input_salary(new_salary)
                break
            except IncorrectInputSalary as e:
                print(e)
        try:
            self.edit.update_edit_salary(index, new_salary)
        except CSVFileNotFoundError as e:
            print(e)