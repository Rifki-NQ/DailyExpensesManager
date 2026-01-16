import pandas as pd
import yaml
from pathlib import Path
from core.exceptions import (CSVFileNotFoundError, YAMLFileNotFoundError, IncorrectTimeFormatError,
                             EmptySalaryDataError, EmptyConfigDataError, InvalidInputIndexError,
                             InvalidFileTypeError)

class CheckInput:
    @staticmethod
    def check_digit(value, min_value, max_value, quit_option: bool | None = None) -> bool:
        if value.isdigit() and min_value <= int(value) <= max_value:
            return True
        elif quit_option and value.lower() == "q":
            return False
        elif value.isdigit():
            raise InvalidInputIndexError("invalid inputted index!")
        else:
            raise InvalidInputIndexError("inputted index must be in digit!")
        
class DataIO:
    @staticmethod
    def create_dataio(file_path: str | Path, file_type: str) -> DataIO | DataIO:
        path = Path(file_path)
        if not path.exists() and file_type.lower() == "csv":
            raise CSVFileNotFoundError(f"failed to read/write ({path}) because the file does not exist!")
        elif not path.exists() and file_type.lower() == "yaml":
            raise YAMLFileNotFoundError(f"failed to read/write ({path}) because the file does not exist!")
        if file_type.lower() == "csv":
            return CSVFileHandler(file_path)
        elif file_type.lower() == "yaml":
            return YAMLFileHandler(file_path)
        else:
            raise InvalidFileTypeError("invalid file type provided!")
    
class CSVFileHandler(DataIO):
    def __init__(self, file_path: str | Path):
        self.file_path = file_path
    
    def read(self) -> pd.DataFrame:
        try:
            pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except pd.errors.EmptyDataError:
            raise EmptySalaryDataError(f"failed to read ({self.file_path}) because the file is empty!")
         
    def save(self, df):
        try:
            df.to_csv(self.file_path, index=False)
        except FileNotFoundError:
            raise CSVFileNotFoundError("incorrect csv file path provided to dump sorted salary data!")
         
class YAMLFileHandler(DataIO):
    def __init__(self, file_path: str | Path):
        self.file_path = file_path
    
    def read(self) -> dict[str, int] | dict[str: None]:
        with open(self.file_path, "r") as file:
            config_data = yaml.safe_load(file)
        if isinstance(config_data, str):
            raise EmptyConfigDataError(f"failed to read ({self.file_path}) because it contains invalid config data!")
        elif config_data is None:
            raise EmptyConfigDataError(f"failed to read ({self.file_path}) because the file is empty!")
        return config_data
        
    def save(self, data):
        with open(self.file_path, "w+") as file:
            yaml.safe_dump(data, file, sort_keys=False)
            
class Sorter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def sort_date(self, df: pd.DataFrame, initial_format: str, after_format: str | None = None) -> pd.DataFrame | None:
        try:
            df["date"] = pd.to_datetime(df["date"], format=initial_format)
        except ValueError as e:
            raise IncorrectTimeFormatError("failed to format the date because the format is not valid!")
        df.sort_values("date", inplace=True)
        if after_format is None:
            return df
        df["date"] = df["date"].dt.strftime(after_format)
        return df