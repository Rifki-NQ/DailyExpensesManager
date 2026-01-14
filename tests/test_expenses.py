import pytest
from core.expenses.expenses_cli import ExpensesCLI

def test_expenses():
    expenses = ExpensesCLI()
    assert len(expenses.monthly_expenses["necessary"]) == 6