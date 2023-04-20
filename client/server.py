import json
import socket

import exceptions
from dto import User, UserItem, Item
from user import UserService


class Server:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(('127.0.0.1', 5000))

    def login(self, username: str) -> None:
        response = self._send_message(f'login;{username}')
        self._update_user(response)

    @staticmethod
    def get_user(username: str) -> User:
        user = server._send_message(f'get;user;{username}')
        user = User(**json.loads(user))
        user.items = [UserItem(**item) for item in user.items]
        return user

    def get_all_usernames(self) -> str:
        usernames = self._send_message('get;users;username')
        return usernames

    @staticmethod
    def get_all_items() -> list[Item]:
        items = server._send_message('get;shop;items')
        items = json.loads(items)
        items = [Item(**json.loads(item)) for item in items]
        return items

    def buy_item(self, item_name: str, count: int = 1) -> None:
        response = server._send_message(f'set;shop;{item_name.capitalize()};{count}')
        if response == 'InsufficientFunds':
            raise exceptions.InsufficientFundsException()
        self._update_user(response)

    def sell_item(self, item_name: str, count: int = 1) -> None:
        response = server._send_message(f'sell;{item_name.capitalize()};{count}')
        if response == 'InsufficientFunds':
            raise exceptions.InsufficientFundsException()
        self._update_user(response)

    def _send_message(self, message: str) -> str:
        self._socket.send(message.encode('utf-8'))
        response = self._socket.recv(4096)
        return response.decode('utf-8')

    @staticmethod
    def _update_user(response: str) -> None:
        user = User(**json.loads(response))
        user.items = [UserItem(**item) for item in user.items]
        UserService.set_authorized_user(user)


server = Server()
