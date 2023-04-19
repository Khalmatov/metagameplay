import json
from contextvars import ContextVar
from typing import Literal


from dto import User, UserItem, Item
from server import server
from user import UserService

state: ContextVar[Literal['login', 'game', 'shop', 'buy', 'sell']] = ContextVar('state', default='login')


def print_profile():
    user = UserService.get_authorized_user()
    items_string = '\n'.join(f'\t{item.name}: {item.count} шт' for item in user.items)
    print(f'\nВаши данные:\n  никнейм: {user.name}\n  баланс: {user.balance}\n  инвентарь:\n{items_string}')


def print_shop():
    items = server.send_message('get;shop;items')
    items = json.loads(items)
    items = [Item(**json.loads(item)) for item in items]
    print("\n{:<8} {:<15}".format('Название', 'Цена'))
    for item in items:
        print("{:<8} {:<15}".format(item.name, item.price))
    state.set('shop')


def print_login():
    users = server.send_message('get;users;username')
    print(f'\nСписок существующих никнеймов: {users}')
    username = input('Введите существующий или новый никнейм: ')
    user = server.send_message(f'login;{username}')
    user = User(**json.loads(user))
    user.items = [UserItem(**item) for item in user.items]
    UserService.set_authorized_user(user)
    state.set('game')
    print_profile()


def buy():
    command = input('Введите название предмета и его количество через пробел (например: щит 3): ')
    item, count = command.strip().split()
    response = server.send_message(f'set;shop;{item.capitalize()};{count}')
    print(f'{response=}')
    if response == 'InsufficientFunds':
        print('Не хватает средств для совершения покупки')
    else:
        print(f'\nКуплен {item} в количестве {count} шт.')
        user = User(**json.loads(response))
        user.items = [UserItem(**item) for item in user.items]
        UserService.set_authorized_user(user)
        print_profile()
        state.set('shop')
        print_shop()


def main():
    print('Добро пожаловать в Метагеймплей!')
    if UserService.is_user_authorized():
        print_profile()
        state.set('game')
    while True:
        match state.get():
            case 'login':
                print_login()
            case 'shop':
                command = input('\nВыберите действие: КУПИТЬ [B], ПРОДАТЬ [S], НАЗАД [C], ВЫЙТИ [Q]: ')
                match command.upper():
                    case 'B':
                        state.set('buy')
                    case 'S':
                        state.set('sell')
                    case 'C':
                        state.set('game')
                    case 'Q':
                        print('До свидания!')
                        break
            case 'buy':
                buy()
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
