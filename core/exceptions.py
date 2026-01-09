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

class MissingSimulationIndexError(EmptyDataAppError):
    """Raised when config data return empty current_simulation_index"""
    pass
        
class FileNotFoundAppError(FileError):
    """Raised when file is not found"""
    pass

class CSVFileNotFoundError(FileNotFoundAppError):
    """Raised when CSV file is not found"""
    pass

class ConfigFileNotFoundError(FileNotFoundAppError):
    """Raised when Config file is not found"""
    pass

class InvalidInputIndexError(AppError):
    """Raised when inputted value is not in the allowed range"""
    pass