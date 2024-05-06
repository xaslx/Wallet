import pytest
from wallet import Wallet
from income import Income
from purchase import Purchase
from exceptions import NotEnoughtMoney

@pytest.fixture
def wallet():
    return Wallet(5000)

@pytest.fixture
def income(wallet):
    return Income(wallet=wallet, category='Доходы')

@pytest.fixture
def purchase(wallet):
    return Purchase(wallet=wallet, category='Расходы')


def test_income_add_transaction(income: Income):
    before: int = income.get_len_rows()
    income.add_transaction(500.0, 'Зарплата')
    after: int = income.get_len_rows()
    assert after > before

def test_purchase_add_transaction(purchase: Purchase):
    before: int = purchase.get_len_rows()
    purchase.add_transaction(200.0, 'Покупка')
    after: int = purchase.get_len_rows()
    assert after > before

def test_purchase_not_enough_money(purchase: Purchase):
    with pytest.raises(NotEnoughtMoney):
        purchase.add_transaction(999999, 'Покупка')

