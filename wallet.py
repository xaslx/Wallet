from dotenv import get_key

mode: str = get_key('.env', 'MODE')


# путь меняется в зависимости от переменной окружения
file_path: str = 'files/balance.txt' if mode == 'DEV' else 'files/test/balance_test.txt'

class Wallet:

    def __init__(self, balance: float) -> None:
        self.balance_file = file_path
        # устанавливаем начальный баланс, если нету файла, если есть то берем баланс из файла
        self.balance = self._read_balance() if self._balance_file_exists() else balance
        self._save_balance()

    # проверка существует ли файл
    def _balance_file_exists(self) -> bool:
        try:
            with open(self.balance_file, 'r', encoding='utf-8'):
                pass
            return True
        except FileNotFoundError:
            return False

    # сохраняем баланс
    def _save_balance(self) -> None:
        with open(self.balance_file, 'w', encoding='utf-8') as file:
            file.write(str(self.balance))

    # читаем баланс из файла
    def _read_balance(self) -> float:
        with open(self.balance_file, 'r', encoding='utf-8') as file:
            return float(file.read())

    # метод для отображения баланса
    def show_my_balance(self) -> float:
        balance: float = float(self._read_balance())
        return balance

    # метод для изменения баланса
    def edit_balance(self, value: float) -> None:
        current_balance = float(self.show_my_balance())
        self.balance = current_balance - value
        self._save_balance()
