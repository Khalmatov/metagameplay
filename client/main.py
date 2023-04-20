import json
from contextvars import ContextVar

from dto import User, UserItem, Item, States
from server import server
from user import UserService

state: ContextVar[States] = ContextVar('state', default=States.LOGIN)


def print_profile():
    user = UserService.get_authorized_user()
    print(f'\nВаши данные:\n  никнейм: {user.name}\n  баланс: {user.balance}')
    print_inventory()


def print_inventory():
    user = UserService.get_authorized_user()
    print('\nВаш инвентарь:')
    items_string = '\n'.join(f'  {item.name}: {item.count} шт' for item in user.items)
    print(items_string)


def print_shop():
    items = server.send_message('get;shop;items')
    items = json.loads(items)
    items = [Item(**json.loads(item)) for item in items]
    print("\nАссортимент магазина:\n  {:<8} {:<15}".format('Название', 'Цена'))
    for item in items:
        print("  {:<8} {:<15}".format(item.name, item.price))
    state.set(States.SHOP)


def print_login():
    users = server.send_message('get;users;username')
    print(f'\nСписок существующих никнеймов: {users}')
    username = input('Введите существующий или новый никнейм: ')
    user = server.send_message(f'login;{username}')
    user = User(**json.loads(user))
    user.items = [UserItem(**item) for item in user.items]
    UserService.set_authorized_user(user)
    state.set(States.GAME)
    print_profile()


def buy():
    command = input('Введите название предмета и его количество через пробел (например: щит 3) или введите C для отмены: ')
    if command.upper() == 'C':
        state.set(States.SHOP)
        return
    item, count = command.strip().split()
    response = server.send_message(f'set;shop;{item.capitalize()};{count}')
    if response == 'InsufficientFunds':
        print('Не хватает средств для совершения покупки')
    else:
        print(f'\nКуплен {item} в количестве {count} шт.')
        user = User(**json.loads(response))
        user.items = [UserItem(**item) for item in user.items]
        UserService.set_authorized_user(user)
        print_profile()
        print_shop()
    state.set(States.SHOP)


def sell():
    print_inventory()
    print('Что вы хотите продать?')
    command = input('Введите название предмета и его количество через пробел (например: меч 1) или введите C для отмены: ')
    if command.upper() == 'C':
        state.set(States.GAME)
        return
    item, count = command.strip().split()
    response = server.send_message(f'sell;{item.capitalize()};{count}')
    if response == 'InsufficientFunds':
        print('У вас недостаточно позиций для совершения продажи')
        state.set(States.SHOP)
    else:
        print(f'\nПродан {item} в количестве {count} шт.')
        user = User(**json.loads(response))
        user.items = [UserItem(**item) for item in user.items]
        UserService.set_authorized_user(user)
        print_profile()
        state.set(States.GAME)


def main():
    print('Добро пожаловать в Метагеймплей!')
    if UserService.is_user_authorized():
        print_profile()
        state.set(States.GAME)
    while True:
        match state.get():
            case States.LOGIN:
                print_login()
            case States.SHOP:
                command = input('\nВыберите действие: КУПИТЬ [B], ПРОДАТЬ [S], НАЗАД [C], ВЫЙТИ [Q]: ')
                match command.upper():
                    case 'B':
                        state.set(States.BUY)
                    case 'S':
                        state.set(States.SELL)
                    case 'C':
                        state.set(States.GAME)
                    case 'Q':
                        print('До свидания!')
                        break
            case States.BUY:
                buy()
            case States.SELL:
                sell()
            case _:
                command = input('\nВыберите действие: ПРОФИЛЬ [P], МАГАЗИН [M], СМЕНИТЬ АККАУНТ [L], ВЫЙТИ [Q]: ')
                match command.upper():
                    case 'P':
                        print_profile()
                    case 'M':
                        print_shop()
                    case 'L':
                        print_login()
                    case 'Q':
                        print('До свидания!')
                        break


if __name__ == '__main__':
    main()
