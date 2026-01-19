from core.utils import DataIO
from pathlib import Path
import pytest

def test_read_salary_config():
    config_handler = DataIO.create_dataio(Path("data/config.yaml"))
    salary_handler = DataIO.create_dataio(Path("data/salary_data.csv"))
    df_salary = salary_handler.read()
    data = config_handler.read()
    df_salary = df_salary.loc[df_salary["date"] == data["current_simulation_date"]].iloc[0].tolist()
    assert df_salary == ["12-2025", 9983450]