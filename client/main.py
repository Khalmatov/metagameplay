from typing import NoReturn

from enums import State, Command
from printer import Printer
from server import server
from state import set_state, get_state
from user import UserService
from shop import Shop


def event_loop() -> NoReturn:
    while True:
        match get_state():
            case State.LOGIN:
                Printer.print_login()
                Printer.print_profile()
                set_state(State.GAME)
            case State.SHOP:
                command = input('\nВведите действие: '
                                'КУПИТЬ [B], ПРОДАТЬ [S], АССОРТИМЕНТ [A], ИНВЕНТАРЬ [I], НАЗАД [C], ВЫЙТИ [Q]: ')
                match command.upper():
                    case Command.BUY:
                        set_state(State.BUY)
                    case Command.SELL:
                        set_state(State.SELL)
                    case Command.INVENTORY:
                        Printer.print_inventory()
                    case Command.CANCEL:
                        set_state(State.GAME)
                    case Command.QUIT:
                        print('До свидания!')
                        break
            case State.BUY:
                Shop.buy_item()
            case State.SELL:
                Shop.sell_item()
            case _:
                command = input('\nВыберите действие: ПРОФИЛЬ [P], МАГАЗИН [M], СМЕНИТЬ АККАУНТ [L], ВЫЙТИ [Q]: ')
                match command.upper():
                    case Command.PROFILE:
                        Printer.print_profile()
                    case Command.SHOP:
                        Printer.print_shop()
                        set_state(State.SHOP)
                    case Command.LOGIN:
                        Printer.print_login()
                    case Command.QUIT:
                        print('До свидания!')
                        break


def main():
    print('Добро пожаловать в MetaGameplay!')
    if username := UserService.get_current_username():
        user = server.get_user(username)
        UserService.set_authorized_user(user)
        Printer.print_profile()
        set_state(State.GAME)
    else:
        set_state(State.LOGIN)
    event_loop()


if __name__ == '__main__':
    main()
