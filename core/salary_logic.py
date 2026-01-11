import pandas as pd
from core.utils import DataIO, CheckInput, Sorter
from core.exceptions import MissingSimulationIndexError

class SalaryBase:
    def __init__(self):
        self.simulation_index = 0
        self.salary_data_filepath = "data/salary_data.csv"
        self.config_filepath = "data/config.yaml"
        self.sorter = Sorter(self.salary_data_filepath)
        self.salary_handler = DataIO(self.salary_data_filepath)
        self.config_handler = DataIO(self.config_filepath)

    def sort_salary_date(self, df: pd.DataFrame) -> pd.DataFrame:
        self.sorter.sort_date(df, initial_format="%m-%Y", after_format="%m-%Y")
        return df
    
    def get_all_salary(self) -> pd.DataFrame:
        all_salary = self.salary_handler.read_csv()
        all_salary.index = all_salary.index + 1
        return all_salary

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
    def check_inputted_index(self, index, min_value, max_value) -> bool:
        if CheckInput.check_digit(index, min_value, max_value):
            return True
    
    def update_current_simulation(self, index):
        index = int(index)
        index -= 1
        updated_simulation = {"current_simulation_index": index}
        self.config_handler.save_config(updated_simulation)
        
class AddNewSalary(SalaryBase):
    def input_new_salary(self):
        pass
    
    def _input_salary_date(self):
        pass
    
    def _input_salary_values(self):
        pass
    
    def check_input_date(self, date):
        salary_data = self.get_all_salary()
        salary_data_date = salary_data["date"].copy()
        pass
    
    def _check_duplicate_date(self, date):
        pass
    
    def _handle_duplicate_date_salary(self):
        self._resolve_duplicate_date_salary()
        pass
    
    def _resolve_duplicate_date_salary(self):
        pass