from time import sleep
from exceptions import NotEnoughtMoney
from transaction import Transaction
from wallet import Wallet
from income import Income
from purchase import Purchase


# если файла 'files/balance.txt' нет то изначальный баланас будет равен 10000.0
# если файл уже имеется, то баланс берется из файла
wallet: Wallet = Wallet(10000.0)
income: Income = Income(wallet=wallet, category='Доходы')
purchase: Purchase = Purchase(wallet=wallet, category='Расходы')


def exit_app() -> None:
    print('Выход из приложения.....')
    sleep(1)
    exit()

def show_balance() -> None:
    print(wallet.show_my_balance())


def add_purchase() -> None:
    while True:
        try:
            amount = float(input('Введите цену: '))
            break
        except ValueError:
            print('Введите только цифры!')
    description: str = input('Введите описание: ') or 'Другое'
    try:
        purchase.add_transaction(amount, description)
        print('Успешно добавлено - категория: Расходы')
    except NotEnoughtMoney:
        print('Недостаточно средств на счету.')


def add_income() -> None:
    while True:
        try:
            amount = float(input('Введите полученную сумму: '))
            break
        except ValueError:
            print('Введите только цифры!')
    description: str = input('Введите описание: ') or 'Другое'
    income.add_transaction(float(amount), description)
    print('Успешно добавлено - категория: Доходы')


def edit_transaction() -> None:
    transaction: str = input('Введите ID транзакции: ').strip()
    Transaction.edit_transaction(id=transaction)


def find_transaction() -> None:
    while True:
        find: str = input('Введите [Дата - поиск по дате, Сумма - поиск по сумме, ID - поиск по id]: ')
        if find == 'Дата':
            date: str = input('Введите дату. Например 2020-05-01: ')
            Transaction.find_transaction('Дата', data=date)
            break
        elif find == 'Сумма':
            amount: str = input('Введите точную сумму: ')
            Transaction.find_transaction('Сумма', data=amount)
            break
        elif find == 'ID':
            ID: str = input('Введите ID: ')
            Transaction.find_transaction('ID', data=ID)
            break
        else:
            print('Введите верные данные')