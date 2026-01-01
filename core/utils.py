import pandas as pd

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
    def __init__(self, file_path):
        self.file_path = file_path
        
    def read_csv(self) -> pd.DataFrame | None:
        try:
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError as e:
            print(f"failed to read {e.filename} because the file does not exist!")
            return None
        except pd.errors.EmptyDataError:
            if self.file_path == "data/salary_data.csv":
                print("failed to read the salary data because it's empty!")
                return None
            else:
                print("failed to read the data because it's empty!")
                return None