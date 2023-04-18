from server import server


def main():
    users = server.send_message('get;users;username')
    print('Добро пожаловать в Метагеймплей!')
    print(f'Список существующих никнеймов: {users}')
    username = input('Введите существующий или новый никнейм: ')
    response = server.send_message(f'login;{username}')
    print(response)


if __name__ == '__main__':
    main()