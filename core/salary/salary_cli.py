from core.exceptions import (FileError, EmptyDataAppError, DuplicatedDateError,
                             InvalidInputIndexError, YAMLFileNotFoundError,
                             IncorrectTimeFormatError, IncorrectInputSalary,
                             CSVFileNotFoundError)

class SalaryCLI:
    def __init__(self, salary_logic, currrent_salary_simulation,
                 change_salary_simulation, add_new_salary,
                 edit_salary, delete_salary):
        self.salary_utils = salary_logic
        self.show = currrent_salary_simulation
        self.change = change_salary_simulation
        self.add = add_new_salary
        self.edit = edit_salary
        self.delete = delete_salary
        self.handle_duplicated_date = False
    
    #helper to input and validate inputted index
    def prompt_index(self, message: str, min_value: int, max_value: int) -> int:
        while True:
            try:
                index = input(message)
                if self.salary_utils.check_input_index(index, min_value, max_value):
                    return int(index)
            except InvalidInputIndexError as e:
                print(e)
    
    def show_current_simulation(self) -> None:
        try:
            current_simulation = self.show.load_salary_simulation()
            print(f"------ Current simulation Date: {current_simulation[0]} ------")
            print(f"----- Current simulation Salary: {current_simulation[1]} -----")
        except FileError as e:
            print(e)
            return
            
    def change_current_simulation(self) -> None:
        try:
            all_salary = self.change.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        index = self.prompt_index("Select which simulation to load (by index): ", 1, len(all_salary))
        try:
            self.change.update_current_simulation(index)
            print("Simulation changed successfully!")
        except YAMLFileNotFoundError as e:
            print(e)
        
    def add_new_salary(self) -> None:
        self.add.reset()
        self.handle_duplicated_date = False
        #input new date then validate
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
            index = self.prompt_index("Decision (by index): ", 1, 3)
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
            
    def edit_salary(self) -> None:
        try:
            all_salary = self.edit.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        index = self.prompt_index("Select which salary to edit (by index): ", 1, len(all_salary))
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
            
    def delete_salary(self) -> None:
        try:
            all_salary = self.delete.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        index = self.prompt_index("Select which salary to delete (by index): ", 1, len(all_salary))
        try:
            self.delete.update_delete_salary(index)
        except CSVFileNotFoundError as e:
            print(e)