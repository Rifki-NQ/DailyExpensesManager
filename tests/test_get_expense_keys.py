from core.expenses.expenses_logic import ExpensesKey
from core.utils import DataIO
from pathlib import Path

def test_get_header():
    yaml_handler = DataIO.create_dataio(Path("data/monthly_expenses.yaml"))
    handler = ExpensesKey(yaml_handler)
    
    headers = handler.get_expenses_header()
    keys = handler.get_expenses_keys()
    
    assert headers == ["necessary", "savings", "free_to_spend"]
    assert keys == ["meal", "electricity", "parents", "fuel", "installment",
                    "internet", "reksa_dana", "gold", "subscription"]