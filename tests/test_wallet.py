from wallet import Wallet


wallet = Wallet(5000)

# Уменьшение баланса
def test_edit_balance():
    before: float = wallet.show_my_balance()
    wallet.edit_balance(500)
    after: float = wallet.show_my_balance()
    assert after < before

# Увеличение баланса  
def test_edit_balance_add():
    before: float = wallet.show_my_balance()
    wallet.edit_balance(-500)
    after: float = wallet.show_my_balance()
    assert after > before