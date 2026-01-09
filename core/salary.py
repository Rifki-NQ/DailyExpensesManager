import pandas as pd
from core.utils import DataIO, CheckInput, Sorter
from core.exceptions import MissingSimulationIndexError, EmptyDataAppError, FileError
from core.exceptions import InvalidInputIndexError, ConfigFileNotFoundError

class SalaryLogic:
    def __init__(self):
        self.simulation_index = 0
        self.salary_data_filepath = "data/salary_data.csv"
        self.config_filepath = "data/config.yaml"
        self.sorter = Sorter(self.salary_data_filepath)
        self.salary_handler = DataIO(self.salary_data_filepath)
        self.config_handler = DataIO(self.config_filepath)
    
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
    
    def get_all_salary(self) -> pd.DataFrame:
        all_salary = self.salary_handler.read_csv()
        all_salary.index = all_salary.index + 1
        return all_salary
    
    def check_inputted_index(self, index, min_value, max_value) -> bool:
        if CheckInput.check_digit(index, min_value, max_value):
            return True
    
    def update_current_simulation(self, index):
        index = int(index)
        index -= 1
        updated_simulation = {"current_simulation_index": index}
        self.config_handler.save_config(updated_simulation)

class SalaryCLI:
    def __init__(self):
        self.salary_logic = SalaryLogic()
    
    def show_current_simulation(self):
        try:
            current_simulation = self.salary_logic.load_salary_simulation()
            print(current_simulation)
        except FileError as e:
            print(e)
            return
            
    def change_current_simulation(self):
        try:
            all_salary = self.salary_logic.get_all_salary()
            print(all_salary)
        except EmptyDataAppError as e:
            print(e)
            return
        while True:
            try:
                index = input("Select which simulation to load (by index): ")
                if self.salary_logic.check_inputted_index(index, 1, len(all_salary)):
                    break
            except InvalidInputIndexError as e:
                print(e)
        try:
            self.salary_logic.update_current_simulation(index)
        except ConfigFileNotFoundError as e:
            print(e)
            return
        print("Simulation changed successfully!")