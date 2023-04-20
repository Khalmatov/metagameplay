import json
import socket
import sys
from select import select

import users
import shop
import exceptions
import db
from enums import Command

to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_sock):
    client_socket, _ = server_sock.accept()
    to_monitor.append(client_socket)


def accept_message(client_socket):
    try:
        request = client_socket.recv(4096)
    except (ConnectionRefusedError, ConnectionResetError):
        close_connection(client_socket)
        return

    if not request:
        close_connection(client_socket)
        return

    message = request.decode("utf-8").split(';')
    match message[0]:
        case Command.LOGIN:
            _, username = message
            user = users.authenticate(username=username)
            response = user.as_json()
        case Command.GET:
            _, obj, item = message
            match obj:
                case 'user':
                    user = users.get_user(username=item)
                    response = user.as_json()
                case 'users':
                    match item:
                        case 'username':
                            response = ', '.join(users.get_all_usernames()) or 'пользователи не обнаружены'
                case 'shop':
                    match item:
                        case 'items':
                            items = shop.get_items()
                            response = json.dumps([item.as_json() for item in items])
        case Command.SET:
            match message[1]:
                case 'shop':
                    _, _, item, count = message
                    try:
                        user = shop.buy_item(item, int(count))
                        response = user.as_json()
                    except exceptions.InsufficientFundsException:
                        response = 'InsufficientFunds'
        case Command.SELL:
            _, item, count = message
            try:
                user = shop.sell_item(item, int(count))
                response = user.as_json()
            except exceptions.InsufficientFundsException:
                response = 'InsufficientFunds'
        case _:
            response = 'че?'
    client_socket.send(response.encode('utf-8'))


def close_connection(client_socket):
    to_monitor.remove(client_socket)
    client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                accept_message(sock)


if __name__ == '__main__':
    print('Сервер запущен')
    db.create_tables_if_not_exists()
    to_monitor.append(server_socket)
    try:
        event_loop()
    except KeyboardInterrupt:
        server_socket.close()
        print('Bye!')
        sys.exit(0)
