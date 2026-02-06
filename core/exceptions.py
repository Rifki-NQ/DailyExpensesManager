class AppError(Exception):
    """Base exception for all app related error"""
    pass

class FileError(AppError):
    """Raised for file or value from file error"""
    pass

class EmptyDataAppError(FileError):
    """Raised when the data file return completely empty data"""
    pass
        
class EmptySalaryDataError(EmptyDataAppError):
    """Raised when salary file return completely empty data"""
    pass
        
class EmptyConfigDataError(EmptyDataAppError):
    """Raised when config file return completely empty data"""
    pass

class MissingSimulationDateError(EmptyDataAppError):
    """Raised when config data return empty current_simulation_date"""
    pass

class InvalidSimulationDateError(EmptyDataAppError):
    """Raised when current_simulation_date in the config does not exist in the salary data"""
    pass
        
class FileNotFoundAppError(FileError):
    """Raised when file is not found"""
    pass

class CSVFileNotFoundError(FileNotFoundAppError):
    """Raised when CSV file is not found"""
    pass

class YAMLFileNotFoundError(FileNotFoundAppError):
    """Raised when Config file is not found"""
    pass

class InvalidFileTypeError(FileNotFoundAppError):
    """Raised when an invalid file type is provided (not CSV or YAML)"""
    pass

class IndexError(AppError):
    """Raised when inputted index is invalid"""
    pass

class InvalidExpenseIndexError(IndexError):
    """Raised when provided expense index is out of range"""
    pass

class InvalidInputIndexError(IndexError):
    """Raised when inputted value is not in the allowed range"""
    pass

class TimeError(FileError):
    """Raised when there is any time related error when handling file"""

class IncorrectTimeFormatError(TimeError):
    """Raised when inputted format of datetime is not valid with what is in the data"""
    pass

class DuplicatedDateError(TimeError):
    """Raised when inputted new date is already exist inside the data"""
    pass

class IncorrectInputSalary(FileError):
    """Raised when inputted salary is not valid"""
    pass

class InvalidDaysLengthError(TimeError):
    """Raised when inputted days length is invalid"""
    pass