import pandas as pd
from core.utils import DataIO, CheckInput, Sorter
from core.exceptions import EmptySimulationIndexError, CSVFileNotFoundError
from core.exceptions import EmptySalaryDataError, EmptyConfigDataError

class SalaryLogic:
    def __init__(self):
        self.simulation_index = 0
        self.salary_data_filepath = "data/salary_data1.csv"
        self.config_filepath = "data/config.yaml"
        self.sorter = Sorter(self.salary_data_filepath)
        self.salary_handler = DataIO(self.salary_data_filepath)
        self.config_handler = DataIO(self.config_filepath)
    
    def _load_simulation_index(self):
        config = self.config_handler.read_config()
        if config["current_simulation_index"] is None:
            raise EmptySimulationIndexError("Empty simulation index from the config!")
        else:
            return config["current_simulation_index"]
            
    def load_salary_simulation(self):
        self.simulation_index = self._load_simulation_index()
        try:
            df_salary = self.salary_handler.read_csv()
        except FileNotFoundError as e:
            raise CSVFileNotFoundError(f"failed to read {self.salary_data_filepath} because the file does not exist!")
        except pd.errors.EmptyDataError:
            raise EmptySalaryDataError("failed to read the data because it's empty!")
        df_salary = df_salary.iloc[self.simulation_index].tolist()
        current_salary_simulation = df_salary
        #convert np.int64 to int
        current_salary_simulation[1] = int(current_salary_simulation[1])
        return current_salary_simulation
    
    def _get_all_salary(self):
        all_salary = self.salary_handler.read_csv()
        if all_salary is None:
            return
        all_salary.index = all_salary.index + 1
        return all_salary
    
    def change_current_simulation(self):
        salary_data = self._get_all_salary()
        print(salary_data)
        while True:
            index = input("Select which simulation to load (by index): ")
            if CheckInput.check_digit(index, 1, len(salary_data)):
                index = int(index)
                index -= 1
                break
        updated_simulation = {"current_simulation_index": index}
        self.config_handler.save_config(updated_simulation)
        print("Simulation changed successfully!")

class SalaryCLI:
    def __init__(self):
        self.salary_logic = SalaryLogic()
    
    def show_current_simulation(self):
        try:
            current_simulation = self.salary_logic.load_salary_simulation()
            print(current_simulation)
        except EmptySimulationIndexError as e:
            print(e)
        except CSVFileNotFoundError as e:
            print(e)
        except EmptySalaryDataError as e:
            print(e)