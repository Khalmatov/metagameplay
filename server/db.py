import sqlite3

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()


def create_tables():
    cursor.execute('CREATE TABLE users(username CHAR(50) PRIMARY KEY, password VARCHAR(128))')
    cursor.execute('CREATE TABLE items(name CHAR(50) PRIMARY KEY, price INT)')
    cursor.execute('''
        CREATE TABLE credits
            (
                username CHAR(50),
                balance  INT,
                PRIMARY KEY (username, balance),
                CHECK (balance >= 0),
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
            )
        ''')
    cursor.execute('''
        CREATE TABLE inventory
            (
                username CHAR(50),
                item CHAR(50),
                count INT,
                PRIMARY KEY (username, item),
                CHECK ( count >= 0 ),
                FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE,
                FOREIGN KEY (item) REFERENCES items (name) ON DELETE CASCADE
            )
    ''')


def create_user(username: str, password: bytes):
    cursor.execute('INSERT INTO users(username, password) VALUES(?, ?)', (username, password))
    con.commit()
    return cursor.lastrowid


def get_user_password(username: str):
    res = cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    return res.fetchone()[0]


def get_user_balance(username: str):
    res = cursor.execute('SELECT password FROM credits WHERE username=?', (username,))
    return res.fetchone()[0]




def init():
    create_tables()
