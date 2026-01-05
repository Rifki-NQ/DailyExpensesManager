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
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_csv(self) -> pd.DataFrame | None:
        try:
            pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError as e:
            print(f"failed to read {e.filename} because the file does not exist!")
            return None
        except pd.errors.EmptyDataError:
            print("failed to read the data because it's empty!")
            return None
         
    def read_config(self):
        try:
            with open(self.file_path, "r") as file:
                config_data = yaml.safe_load(file)
            return config_data
        except FileNotFoundError as e:
            print(f"failed to read {e.filename} because the file does not exist!")
            return None
        
    @staticmethod
    def save_config(data):
        try:
            with open("data/config.yaml", "w") as file:
                yaml.safe_dump(data, file, sort_keys=False)
        except yaml.YAMLError as e:
            print(e)
            
class Sorter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def sort_date(self, initial_format: str, after_format: str | None = None) -> pd.DataFrame | None:
        df = DataIO.read_csv(self.file_path)
        try:
            df["date"] = pd.to_datetime(df["date"], format=initial_format)
        except ValueError as e:
            print(f"date format error: {e}")
            return None
        df.sort_values("date", inplace=True)
        if after_format is None:
            return df
        df["date"] = df["date"].dt.strftime(after_format)
        return df