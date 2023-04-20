from server import server
from user import UserService


class Printer:

    @staticmethod
    def print_login() -> None:
        usernames = server.get_all_usernames()
        print(f'\nСписок существующих никнеймов: {usernames}')
        username = input('Введите существующий или новый никнейм: ')
        server.login(username)

    @classmethod
    def print_profile(cls) -> None:
        user = UserService.get_authorized_user()
        print(f'\nВаши данные:\n  никнейм: {user.name}\n  баланс: {user.balance}')
        cls.print_inventory()

    @staticmethod
    def print_shop() -> None:
        print("\nАссортимент магазина:\n  {:<8} {:<15}".format('Название', 'Цена'))
        for item in server.get_all_items():
            print("  {:<8} {:<15}".format(item.name, item.price))

    @staticmethod
    def print_inventory() -> None:
        user = UserService.get_authorized_user()
        print('\nВаш инвентарь:')
        items_string = '\n'.join(f'  {item.name}: {item.count} шт' for item in user.items)
        print(items_string)
