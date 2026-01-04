import pandas as pd
from core.utils import DataIO

class Salary:
    def __init__(self):
        self.simulation_index = 0
    
    def _load_simulation_index(self):
        config = DataIO.read_config()
        if config["current_simulation_index"] is None:
            print("Empty simulation index from the config!")
            return None
        else:
            return config["current_simulation_index"]
    
    def show_current_simulation(self):
        current_simulation = self._load_salary_simulation()
        print(current_simulation)
            
    def _load_salary_simulation(self):
        self.simulation_index = self._load_simulation_index()
        df_salary = DataIO.read_csv("data/salary_data.csv")
        if self.simulation_index is None or df_salary is None:
            return
        df_salary = df_salary.iloc[self.simulation_index].tolist()
        current_salary_simulation = df_salary
        #convert np.int64 to int
        current_salary_simulation[1] = int(current_salary_simulation[1])
        return current_salary_simulation