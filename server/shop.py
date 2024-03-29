from dto import Item, User

import db
from users import UserService
import exceptions


def get_items() -> list[Item]:
    items = db.get_all_items()
    return items


def buy_item(item_name: str, count: int = 1) -> User:
    user = UserService.get_authorized_user()
    user_balance = db.get_user_balance(user.name)
    item = db.get_item(item_name)
    if user_balance < (item.price * count):
        raise exceptions.InsufficientFundsException()
    db.add_item_to_user_inventory(username=user.name, item=item, count=count)
    db.subtract_user_credits(username=user.name, count=item.price * count)
    user.balance -= item.price * count
    user.items = db.get_user_items(username=user.name)
    UserService.set_authorized_user(user)
    return user


def sell_item(item_name: str, count: int = 1) -> User:
    user = UserService.get_authorized_user()
    user_item_count = db.get_user_item_count(username=user.name, item_name=item_name)

    if count > user_item_count:
        raise exceptions.InsufficientFundsException()

    db.delete_item_from_user_inventory(username=user.name, item_name=item_name, count=count)
    item = db.get_item(item_name)
    db.add_user_credits(username=user.name, count=count * item.price)
    user.balance = db.get_user_balance(user.name)
    user.items = db.get_user_items(user.name)
    UserService.set_authorized_user(user)
    return user
