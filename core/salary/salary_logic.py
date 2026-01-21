import pandas as pd
from pathlib import Path
from core.utils import DataIO, CheckInput, Sorter
from core.exceptions import (MissingSimulationIndexError, DuplicatedDateError,
                             IncorrectTimeFormatError, IncorrectInputSalary)

class SalaryBase:
    def __init__(self):
        self.simulation_date = ""
        self.SALARY_DATA_FILEPATH = Path("data/salary_data.csv")
        self.CONFIG_FILEPATH = Path("data/config.yaml")
        self.salary_handler = DataIO.create_dataio(self.SALARY_DATA_FILEPATH)
        self.config_handler = DataIO.create_dataio(self.CONFIG_FILEPATH)

    def get_all_salary(self) -> pd.DataFrame:
        all_salary = self.salary_handler.read()
        all_salary.index = all_salary.index + 1
        return all_salary
    
    def check_input_index(self, index, min_value, max_value) -> bool:
        if CheckInput.check_digit(index, min_value, max_value):
            return True
        
    def check_input_salary(self, salary: str) -> int:
        if not salary.isdigit():
            raise IncorrectInputSalary("salary must be in digit!")
        elif int(salary) < 0:
            raise IncorrectInputSalary("salary cannot be lower than 0!")
        return int(salary)

class CurrentSalarySimulation(SalaryBase):
    def _load_simulation_date(self) -> int:
        config = self.config_handler.read()
        if config["current_simulation_date"] is None:
            raise MissingSimulationIndexError("empty simulation date from the config!")
        return config["current_simulation_date"]
            
    def load_salary_simulation(self) -> list[str | int]:
        self.simulation_date = self._load_simulation_date()
        df_salary = self.salary_handler.read()
        df_salary = df_salary.loc[df_salary["date"] == self.simulation_date].iloc[0].tolist()
        current_salary_simulation = df_salary
        #convert np.int64 to int
        current_salary_simulation[1] = int(current_salary_simulation[1])
        return current_salary_simulation
    
class ChangeSalarySimulation(SalaryBase):
    def update_current_simulation(self, index) -> None:
        salary_df = self.get_all_salary()
        index = int(index)
        index -= 1
        updated_simulation = {"current_simulation_date": salary_df.iloc[index, 0]}
        self.config_handler.save(updated_simulation)
        
class AddNewSalary(SalaryBase):
    def __init__(self):
        super().__init__()
        self.duplicated_decision = 0
        self.exit_current_process = False
    
    def reset(self) -> None:
        self.duplicated_decision = 0
        self.exit_current_process = False
    
    def check_input_date(self, date: str) -> str:
        salary_data = self.get_all_salary()
        if (salary_data["date"] == date).any():
            raise DuplicatedDateError("the inputted date is already exist in the data")
        try:
            date = pd.to_datetime(date, format="%m-%Y")
            date = date.strftime("%m-%Y")
            return date
        except pd.errors.OutOfBoundsDatetime:
            raise IncorrectTimeFormatError("Out of bound date (allowed year range is '1677' to '2261')")
        except ValueError:
            raise IncorrectTimeFormatError("incorrect/invalid format of inputted date! (must be MM-YYYY)")
            
    def handle_duplicate_date_salary(self, decision: int) -> None:
        if decision == 1:
            self.duplicated_decision = 1
        elif decision == 2:
            self.duplicated_decision = 2
        elif decision == 3:
            self.exit_current_process = True
    
    def update_new_salary(self, new_date: str, new_salary: int) -> None:
        salary_data = self.get_all_salary()
        if self.duplicated_decision == 1:
            salary_data.loc[salary_data["date"] == new_date] = [new_date, new_salary]
        elif self.duplicated_decision == 2:
            duplicated_salary = salary_data.loc[salary_data["date"] == new_date, "salary"].iloc[0]
            new_salary = duplicated_salary +  new_salary
            salary_data.loc[salary_data["date"] == new_date] = [new_date, new_salary]
        else:
            new_salary_df = pd.DataFrame({"date": new_date, "salary": new_salary}, index=[0])
            salary_data = pd.concat([salary_data, new_salary_df], ignore_index=True)
            salary_data = Sorter.sort_date(salary_data, "%m-%Y", "%m-%Y")
        self.salary_handler.save(salary_data)
        
class EditSalary(SalaryBase):
    def update_edit_salary(self, index: int, new_salary: int) -> None:
        salary_data = self.get_all_salary()
        salary_data.loc[index, "salary"] = new_salary
        self.salary_handler.save(salary_data)
        
class DeleteSalary(SalaryBase):
    def update_delete_salary(self, index: int) -> None:
        salary_data = self.get_all_salary()
        salary_data = salary_data.drop(index=index)
        self.salary_handler.save(salary_data)