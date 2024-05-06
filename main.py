from function import (
    exit_app,
    add_income,
    add_purchase,
    edit_transaction,
    find_transaction,
    show_balance,
    income,
    purchase
)
from dotenv import load_dotenv


load_dotenv('.env')


def main():

    menu: str = (
    f'\n---Мой кошелек---\n'
    f'Доступные команды:\n\n'
    f'/help - посмотреть все команды\n'
    f'/balance - посмотреть свой баланс\n'
    f'/add_purchase - добавить расходы\n'
    f'/show_purchases - посмотреть мои расходы\n'
    f'/add_income - добавить доходы\n'
    f'/show_incomes - посмотреть мои доходы\n'
    f'/edit_transaction - редактировать транзакцию\n'
    f'/find_transaction - найти транзакцию\n'
    f'/exit - выйти из приложения')
    
    print(menu)

    commands: dict = {
        '/balance': show_balance,
        '/exit': exit_app,
        '/help': lambda: print(menu),
        '/add_purchase': add_purchase,
        '/show_purchases': lambda: purchase.show_transaction('Расходы'),
        '/add_income': add_income,
        '/show_incomes': lambda: income.show_transaction('Доходы'),
        '/edit_transaction': edit_transaction,
        '/find_transaction': find_transaction
    }
    

    while True:
        command: str = input('\nВведите команду: ').strip()
        action = commands.get(command)
        if action:
            action()
        else:
            print(f'Неизвестная команда, введите /help - чтобы посмотреть список команд')


if __name__ == '__main__':
    main()