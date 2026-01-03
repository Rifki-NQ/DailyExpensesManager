import pandas as pd
import yaml

class CheckInput:
    @staticmethod
    def check_digit(value, min_value, max_value) -> bool:
        if value.isdigit() and min_value <= int(value) <= max_value:
            return True
        elif value.isdigit():
            print("Invalid inputted index!")
            return False
        else:
            print("Inputted index must be in digit!")
            return False
        
class DataIO:
    @staticmethod
    def read_csv(self, file_path) -> pd.DataFrame | None:
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError as e:
            print(f"failed to read {e.filename} because the file does not exist!")
            return None
        except pd.errors.EmptyDataError:
            print("failed to read the data because it's empty!")
            return None
        
    @staticmethod    
    def read_config():
        try:
            with open("data/config.yaml", "r") as file:
                config_data = yaml.safe_load(file)
            return config_data
        except FileNotFoundError as e:
            print(f"failed to read {e.filename} because the file does not exist!")
            return None