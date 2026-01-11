import pandas as pd
from core.utils import DataIO, CheckInput, Sorter
from core.exceptions import (MissingSimulationIndexError, DuplicatedDateError,
                             IncorrectTimeFormatError, IncorrectInputSalary)

class SalaryBase:
    def __init__(self):
        self.simulation_index = 0
        self.salary_data_filepath = "data/salary_data.csv"
        self.config_filepath = "data/config.yaml"
        self.sorter = Sorter(self.salary_data_filepath)
        self.salary_handler = DataIO(self.salary_data_filepath)
        self.config_handler = DataIO(self.config_filepath)
        self.exit_current_process = False

    def sort_salary_date(self, df: pd.DataFrame) -> pd.DataFrame:
        self.sorter.sort_date(df, initial_format="%m-%Y", after_format="%m-%Y")
        return df
    
    def get_all_salary(self) -> pd.DataFrame:
        all_salary = self.salary_handler.read_csv()
        all_salary.index = all_salary.index + 1
        return all_salary
    
    def check_inputted_index(self, index, min_value, max_value) -> bool:
        if CheckInput.check_digit(index, min_value, max_value):
            return True

class CurrentSalarySimulation(SalaryBase):
    def _load_simulation_index(self) -> int:
        config = self.config_handler.read_config()
        if config["current_simulation_index"] is None:
            raise MissingSimulationIndexError("empty simulation index from the config!")
        return config["current_simulation_index"]
            
    def load_salary_simulation(self) -> list[str | int]:
        self.simulation_index = self._load_simulation_index()
        df_salary = self.salary_handler.read_csv()
        df_salary = df_salary.iloc[self.simulation_index].tolist()
        current_salary_simulation = df_salary
        #convert np.int64 to int
        current_salary_simulation[1] = int(current_salary_simulation[1])
        return current_salary_simulation
    
class ChangeSalarySimulation(SalaryBase):
    def update_current_simulation(self, index):
        index = int(index)
        index -= 1
        updated_simulation = {"current_simulation_index": index}
        self.config_handler.save_config(updated_simulation)
        
class AddNewSalary(SalaryBase):
    def __init__(self):
        super().__init__()
        self.duplicated_decision = int
    
    def check_input_date(self, date: str) -> str:
        salary_data = self.get_all_salary()
        if (salary_data["date"] == date).any():
            raise DuplicatedDateError("the inputted date is already exist in the data")
        try:
            date = pd.to_datetime(date, format="%m-%Y")
            date = date.dt.strftime("%m-%Y")
            return date
        except ValueError:
            raise IncorrectTimeFormatError("incorrect format of inputted date! (must be MM-YYYY)")
        except pd.errors.OutOfBoundsDatetime:
            raise IncorrectTimeFormatError("Out of bound date (allowed year range is '1677' to '2261')")
    
    def check_input_salary(self, salary: str):
        if not salary.isdigit():
            raise IncorrectInputSalary("salary must be in digit!")
        elif int(salary) < 0:
            raise IncorrectInputSalary("salary cannot be lower than 0!")
        return int(salary)
            
    def handle_duplicate_date_salary(self, decision: int):
        if decision == 1:
            self.duplicated_decision = 1
        elif decision == 2:
            self.duplicated_decision = 2
        elif decision == 3:
            self.exit_current_process = True
    
    def update_new_salary(self, new_date, new_salary):
        salary_data = self.get_all_salary()
        new_data = [new_date, new_salary]
        if self.duplicated_decision == 1:
            salary_data.loc[salary_data["date"] == new_date] = new_data
            self.salary_handler.save_csv(salary_data)
        elif self.duplicated_decision == 2:
            pass