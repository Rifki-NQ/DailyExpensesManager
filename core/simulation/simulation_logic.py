from core.exceptions import (InvalidDaysLengthError)

class DailyExpensesLogic():
    def validate_days_length(self, value: str) -> bool:
        if value.isdigit() and int(value) < 1:
            raise InvalidDaysLengthError("Days length cannot below 1!")
        elif value.isdigit() and int(value) > 31:
            raise InvalidDaysLengthError("Days length cannot be over 31 days!")
        elif value.isdigit():
            return True
        else:
            raise InvalidDaysLengthError("Days length must be in digit!")