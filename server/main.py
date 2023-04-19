import json
import socket
import sys
from select import select

import users
import shop
import errors

to_monitor = []  # файлы, за которыми следим

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET - Address Family IP4 , SOCK_STREAM - поддержка протокола TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# SOL_SOCKET - опция относится к уровню сокета, SO_REUSERADDR - переиспользование адреса,  1 - значение
server_socket.bind(('localhost', 5000))  # привязываем сокет к 5000 порту локалхоста (127.0.0.1)
server_socket.listen()  # сокет находится в режиме активного слушания порта постоянно


def accept_connection(server_socket):
    """
    Функция запускается при обнаружении нового входящего подключения
    """
    client_socket, addr = server_socket.accept()  # извлекаем сокет клиента и его адрес
    print('У нас новое подключение с адреса:', addr)

    to_monitor.append(client_socket)  # начинаем мониторить над клиентским сокетом


def send_message(client_socket):
    """
    Функция запускается при обнаружении нового сообщения от клиента
    """
    request = client_socket.recv(4096)  # обнаруженный запрос, 4096 - это размер буфера сообщения

    if request:
        message = request.decode("utf-8")
        message = message.split(';')
        print(f'{message=}')
        match message[0]:
            case 'login':
                _, username = message
                user = users.authenticate(username=username)
                response = user.as_json()
            case 'get':
                _, obj, item = message
                match obj:
                    case 'user':
                        user = users.get_user(username=item)
                        response = user.as_json()
                    case 'users':
                        match item:
                            case 'username':
                                response = ', '.join(users.get_all_usernames())
                    case 'shop':
                        match item:
                            case 'items':
                                items = shop.get_items()
                                response = json.dumps([item.as_json() for item in items])
            case 'set':
                match message[1]:
                    case 'shop':
                        _, _, item, count = message
                        try:
                            user = shop.buy(item, int(count))
                            response = user.as_json()
                        except errors.InsufficientFundsException:
                            response = 'InsufficientFunds'
            case _:
                print('ne login')
                response = 'че?'
        client_socket.send(response.encode('utf-8'))
    else:
        print('Клиент отправил нам пустое сообщение, отключаемся от него и перестаем за ним следить')
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    """
    Родительская функция, которая следит за изменением состояния сокетов
    и очередью выполнения определенных функций
    """
    while True:

        print('Ждем изменения файлов\n')
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors
        print('Какой-то файл изменился')

        for sock in ready_to_read:
            print('Перебираем список файлов, которые стали доступны к чтению')
            if sock is server_socket:
                print('Обнаружилось, что файл - это серверный сокет, новое подключение!')
                accept_connection(sock)
            else:
                print('Обнаружилось, что файл - это клиентский сокет, новое сообщение!')
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    try:
        event_loop()
    except KeyboardInterrupt:
        server_socket.close()
        print('Bye!')
        sys.exit(0)
