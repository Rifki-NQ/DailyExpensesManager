import pandas as pd
import yaml
from core.exceptions import CSVFileNotFoundError, ConfigFileNotFoundError
from core.exceptions import EmptySalaryDataError, EmptyConfigDataError
from core.exceptions import InvalidInputtedIndexError, IncorrectConfigFilePath

class CheckInput:
    @staticmethod
    def check_digit(value, min_value, max_value, quit_option: bool | None = None) -> bool:
        if value.isdigit() and min_value <= int(value) <= max_value:
            return True
        elif quit_option and value.lower() == "q":
            return False
        elif value.isdigit():
            raise InvalidInputtedIndexError("invalid inputted index!")
        else:
            raise InvalidInputtedIndexError("inputted index must be in digit!")
        
class DataIO:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_csv(self) -> pd.DataFrame:
        try:
            pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError:
            raise CSVFileNotFoundError(f"failed to read ({self.file_path}) because the file does not exist!")
        except pd.errors.EmptyDataError:
            raise EmptySalaryDataError(f"failed to read ({self.file_path}) because the file is empty!")
         
    def read_config(self) -> dict[str, int] | dict[str: None]:
        try:
            with open(self.file_path, "r") as file:
                config_data = yaml.safe_load(file)
            if isinstance(config_data, str):
                raise EmptyConfigDataError(f"failed to read ({self.file_path}) because it contains invalid config data!")
            elif config_data is None:
                raise EmptyConfigDataError(f"failed to read ({self.file_path}) because the file is empty!")
            return config_data
        except FileNotFoundError:
            raise ConfigFileNotFoundError(f"failed to read ({self.file_path}) because the file does not exist!")
        
    def save_config(self, data):
        if self.file_path != "data/config.yaml":
            raise IncorrectConfigFilePath("incorrect config file path provided to dump the new config!")
        with open(self.file_path, "w") as file:
            yaml.safe_dump(data, file, sort_keys=False)
            
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