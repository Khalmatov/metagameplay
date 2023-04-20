import exceptions
from enums import Commands, State
from printer import Printer
from server import server
from state import set_state


class Shop:

    @staticmethod
    def buy_item() -> None:
        command = input(
            'Введите название предмета и его количество через пробел (например: щит 3) или введите C для отмены: ')
        if command.upper() == Commands.CANCEL:
            set_state(State.SHOP)
            return
        item_name, count = command.strip().split()
        try:
            server.buy_item(item_name=item_name, count=count)
        except exceptions.InsufficientFundsException:
            print('Не хватает средств для совершения покупки')
        else:
            print(f'\nКуплен {item_name} в количестве {count} шт.')
            Printer.print_profile()
            Printer.print_shop()
        set_state(State.SHOP)

    @staticmethod
    def sell_item() -> None:
        Printer.print_inventory()
        print('Что вы хотите продать?')
        command = input(
            'Введите название предмета и его количество через пробел (например: меч 1) или введите C для отмены: '
        )
        if command.upper() == Commands.CANCEL:
            set_state(State.GAME)
            return
        item_name, count = command.strip().split()
        try:
            server.sell_item(item_name=item_name, count=count)
        except exceptions.InsufficientFundsException:
            print(f'У вас нет "{item_name}" в количестве {count} штук')
            set_state(State.SHOP)
        else:
            print(f'\nПродан {item_name} в количестве {count} шт.')
            Printer.print_profile()
            set_state(State.GAME)
