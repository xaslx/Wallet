from datetime import datetime
from wallet import Wallet
import csv
from exceptions import NotEnoughtMoney
from dotenv import get_key


mode: str = get_key('.env', 'MODE')

# путь меняется в зависимости от переменной окружения
file_path: str = 'files/transactions.csv' if mode == 'DEV' else 'files/test/transactions_test.csv'

class Transaction:

    def __init__(self, wallet: Wallet, category: str) -> None:
        self.wallet = wallet
        self.category = category

    # добавление транзакции (расходи или доходы , зависит какая категория передается)
    def add_transaction(self, amount: float, description: str) -> None:
        # нельзя делать расходы больше чем баланс
        if amount > self.wallet.show_my_balance() and self.category == 'Расходы':
            raise NotEnoughtMoney
        if amount < 1:
            while True:
                try:
                    amount = float(input('Введите сумму больше 0: '))
                    if amount > 0:
                        break
                except ValueError:
                    print('Сумма должна состоять только из цифр!')
        # увеличиваем баланс, если категория Доходы
        if self.category == 'Доходы':
            self.wallet.edit_balance(-amount)
        # уменьшаем баланс, если категория Расходы
        else:
            self.wallet.edit_balance(amount)
        # сохраняем транзакцию
        self._save_transaction(amount=amount, description=description)

    # метод для отображения истории (расходов или доходов)
    def show_transaction(self, category: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader: dict = csv.DictReader(file)
                print(f'\nВаша история: ({category})\n')
                for i in reader:
                    # отображаем все строчки связанные с выбранной категорией (Доходы или Расходы)
                    if i['Категория'] == category:
                        print(i)
        except FileNotFoundError:
            print('У вас еще нет транзакций')

    # редактирование транзакций
    @classmethod
    def edit_transaction(cls, id: str) -> None:
        # индекс для поиска нужной транзакции
        transaction_index = None
        # получаем список всех транзакций
        transactions = cls._get_all_transaction()
        if transactions is not None:
            for index, transaction in enumerate(transactions):
                if transaction['ID'] == str(id):
                    transaction_index = index
                    break

            if transaction_index is not None:
                print(transactions[transaction_index])
                res = input('Хотите ли вы редактировать запись? введите (Y-да / N-нет): ').strip().upper()
                if res == 'Y':
                    while True:
                        try:
                            amount = float(input('Введите новую сумму: '))
                            break
                        except ValueError:
                            print('Ошибка! Введите только цифры.')
                    # редактируем транзакцию
                    description = input('Введите новое описание: ')
                    transactions[transaction_index]['Сумма'] = amount
                    transactions[transaction_index]['Описание'] = description

                    # перезаписываем файл
                    cls._rewrite_file(data=transactions)
                    print('Транзакция отредактирована')
                else:
                    print('Вы отменили редактирование')
        else:
            print('Не удалось найти транзакцию')

    # метод для перезаписывания файла
    @staticmethod
    def _rewrite_file(data: list):
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            fieldname: list = ['ID', 'Дата', 'Категория', 'Сумма', 'Описание', 'Баланс']
            writer = csv.DictWriter(file, fieldnames=fieldname)
            writer.writeheader()
            writer.writerows(data)

    # метод для получения всех транзакций
    @staticmethod
    def _get_all_transaction() -> list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file = csv.DictReader(file)
                data: list = []
                for i in file:
                    data.append(i)
                return data
        except FileNotFoundError:
            print('Файл с транзакциями не найден')

    # метод для поиска транзакцию по: [Дате, Сумме или ID]
    @classmethod
    def find_transaction(cls, find_by: str, data: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for i in reader:
                    if i[find_by] == data:
                        print(i)
        except FileNotFoundError:
            print('Файл с транзакциями не найден')

    # проверка существует ли файл
    def _file_exist(self) -> bool:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                pass
            return True
        except FileNotFoundError:
            return False

    # метод для получения количества записей в файле
    def get_len_rows(self) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # получаем количество файлов, если файла нет то возвращаем 0
                return sum(1 for _ in reader)
        except FileNotFoundError:
            return 0

    # сохранение транзакции в csv файл
    def _save_transaction(self, amount: float, description: str) -> None:
        res: bool = self._file_exist()
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            fieldname: list[str] = ['ID', 'Дата', 'Категория', 'Сумма', 'Описание', 'Баланс']
            writer = csv.DictWriter(file, fieldnames=fieldname)
            
            # если файла еще не существует то записываем название для колонок
            # если файл уже есть то просто добавляем новые записи
            if not res:
                writer.writeheader()

            # получаем количество записей для того чтобы записывать ID записи
            id_row: int = self.get_len_rows()
            writer.writerow({
                'ID': id_row + 1 ,
                'Дата': datetime.now().strftime('%Y-%m-%d'),
                'Категория': self.category,
                'Сумма': str(amount),
                'Описание': description,
                'Баланс': str(self.wallet.show_my_balance())
            })
        