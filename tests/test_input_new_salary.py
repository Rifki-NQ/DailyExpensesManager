import pytest
import pandas as pd

def test_input_salary_date():
    df = pd.read_csv("date/salary_data.csv")
    print(df)

if __name__ == "__main__":
    test_input_salary_date()