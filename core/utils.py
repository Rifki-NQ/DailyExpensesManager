import pandas as pd
import yaml
from pathlib import Path
from abc import ABC, abstractmethod
from core.exceptions import (CSVFileNotFoundError, YAMLFileNotFoundError, IncorrectTimeFormatError,
                             EmptySalaryDataError, EmptyDataAppError, InvalidInputIndexError,
                             InvalidFileTypeError)
from typing import Any

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
        
class DataIO(ABC):
    @abstractmethod
    def read(self, **kwargs):
        pass
    
    @abstractmethod
    def save(self, data):
        pass
    
    @staticmethod
    def create_dataio(file_path: Path) -> DataIO:
        valid_file_types = {"csv", "yaml"}
        file_type = file_path.suffix.lstrip(".")
        if not file_type in valid_file_types:
            raise InvalidFileTypeError("invalid file type provided!")
        if not file_path.exists() and file_type == "csv":
            raise CSVFileNotFoundError(f"failed to read/write ({file_path}) because the file does not exist!")
        elif not file_path.exists() and file_type == "yaml":
            raise YAMLFileNotFoundError(f"failed to read/write ({file_path}) because the file does not exist!")
        if file_type == "csv":
            return CSVFileHandler(file_path)
        elif file_type == "yaml":
            return YAMLFileHandler(file_path)
    
class CSVFileHandler(DataIO):
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def read(self, **kwargs) -> pd.DataFrame:
        try:
            pd.set_option("display.max_rows", None)
            df = pd.read_csv(self.file_path)
            return df
        except pd.errors.EmptyDataError:
            raise EmptySalaryDataError(f"failed to read ({self.file_path}) because the file is empty!")
        except FileNotFoundError:
            raise CSVFileNotFoundError(f"failed to read/write ({self.file_path}) because the file does not exist!")
         
    def save(self, df):
        df.to_csv(self.file_path, index=False)
         
class YAMLFileHandler(DataIO):
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def _format_yaml(self, data) -> dict[str, Any]:
        formatted_yaml = yaml.dump(
            data,
            sort_keys=False,
            default_flow_style=False
        )
        return formatted_yaml
    
    def read(self, **kwargs) -> dict[str, Any]:
        format_data = kwargs.get("format_data", False)
        try:
            with open(self.file_path, "r") as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise YAMLFileNotFoundError(f"failed to read/write ({self.file_path}) because the file does not exist!")
        #return error if any data is empty
        if data is None:
            raise EmptyDataAppError(f"failed to read ({self.file_path}) because the file is empty!")
        if format_data:
            data = self._format_yaml(data)
        return data
        
    def save(self, data):
        with open(self.file_path, "w+") as file:
            yaml.safe_dump(data, file, sort_keys=False)
            
class Sorter:
    @staticmethod
    def sort_date(df: pd.DataFrame, initial_format: str, after_format: str | None = None) -> pd.DataFrame:
        try:
            df["date"] = pd.to_datetime(df["date"], format=initial_format)
        except ValueError:
            raise IncorrectTimeFormatError("failed to format the date because the initial format is invalid!")
        df.sort_values("date", inplace=True)
        if after_format is not None:
            df["date"] = df["date"].dt.strftime(after_format)
        return df