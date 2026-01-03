import pandas as pd
from core.utils import DataIO

class Salary:
    def __init__(self):
        pass
    
    def _get_current_simulation(self):
        config = DataIO.read_config()
        return config
    
    def show_current_simulation(self):
        data = self._get_current_simulation()
        if data is not None:
            print(data)