import pytest
from core.utils import DataIO

def test_expenses():
    config = DataIO("data/monthly_expenses.yaml")
    expenses = config.read_config()
    assert expenses["necessary"]["meal"] == 900000