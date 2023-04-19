import json
import socket as s

from dto import User, UserItem


class Server:
    socket: s.socket

    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 5000))

    def send_message(self, message: str) -> str:
        self.socket.send(message.encode('utf-8'))
        response = self.socket.recv(4096)
        return response.decode('utf-8')

    @staticmethod
    def get_user(username: str) -> User:
        user = server.send_message(f'get;user;{username}')
        user = User(**json.loads(user))
        user.items = [UserItem(**item) for item in user.items]
        return user


server = Server()
