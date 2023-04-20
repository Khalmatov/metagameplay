from typing import NoReturn

from enums import State, Commands
from printer import Printer
from server import server
from state import set_state, get_state
from user import UserService
from shop import Shop


def run_loop() -> NoReturn:
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
                    case Commands.BUY:
                        set_state(State.BUY)
                    case Commands.SELL:
                        set_state(State.SELL)
                    case Commands.INVENTORY:
                        Printer.print_inventory()
                    case Commands.CANCEL:
                        set_state(State.GAME)
                    case Commands.QUIT:
                        print('До свидания!')
                        break
            case State.BUY:
                Shop.buy_item()
            case State.SELL:
                Shop.sell_item()
            case _:
                command = input('\nВыберите действие: ПРОФИЛЬ [P], МАГАЗИН [M], СМЕНИТЬ АККАУНТ [L], ВЫЙТИ [Q]: ')
                match command.upper():
                    case Commands.PROFILE:
                        Printer.print_profile()
                    case Commands.SHOP:
                        Printer.print_shop()
                        set_state(State.SHOP)
                    case Commands.LOGIN:
                        Printer.print_login()
                    case Commands.QUIT:
                        print('До свидания!')
                        break


def main():
    print('Добро пожаловать в MetaGameplay!')
    if username := UserService.get_current_username():
        user = server.get_user(username)
        UserService.set_authorized_user(user)
        Printer.print_profile()
        set_state(State.GAME)
    run_loop()


if __name__ == '__main__':
    main()
