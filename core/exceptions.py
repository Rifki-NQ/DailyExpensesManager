class EmptySimulationIndexError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        
class CSVFileNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class EmptySalaryDataError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class EmptyConfigDataError(Exception):
    def __init__(self, message):
        super().__init__(message)