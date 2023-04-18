import sqlite3

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

from dto import Item, Inventory


def create_tables():
    cursor.execute('CREATE TABLE users(username CHAR(50) PRIMARY KEY)')
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
    cursor.execute('''
        INSERT INTO items(name, price) VALUES
            ('Меч', 50),
            ('Кольчуга', 30),
            ('Сапоги', 20),
            ('Шлем', 20),
            ('Щит', 40),
            ('Конь', 300)
    ''')
    con.commit()


def create_user(username: str):
    cursor.execute('INSERT INTO users(username) VALUES(?)', (username,))
    con.commit()
    return cursor.lastrowid


def get_all_users() -> tuple[str] | None:
    res = cursor.execute('SELECT username FROM users')
    return res.fetchone()


def is_user_exists(username: str) -> bool:
    res = cursor.execute('SELECT username FROM users WHERE username=?', (username,))
    return res.fetchone()


def add_credits_to_user(username: str, credits: int):
    cursor.execute('UPDATE credits SET balance = balance + ? WHERE username = ?', (credits, username))
    con.commit()


def get_user_balance(username: str) -> int:
    res = cursor.execute('SELECT balance FROM users WHERE username=?', (username,))
    return res.fetchone()[0]


def get_user_inventory(username: str) -> list[Inventory]:
    res = cursor.execute('SELECT item, count FROM inventory WHERE username=?', (username,))
    return [Inventory(item=i[0], count=i[1]) for i in res.fetchall()]


def get_all_items() -> list[Item]:
    res = cursor.execute('SELECT name, price FROM items')
    return [Item(name=item[0], price=item[1]) for item in res.fetchall()]


def add_item_to_user_inventory(username: str, item: Item, count: int = 1):
    if cursor.execute('SELECT username FROM inventory WHERE username = ? and item = ?',
                      (username, item.name)).fetchone():
        cursor.execute('UPDATE inventory SET count = count + ? WHERE username = ? and item = ?',
                       (count, username, item.name))
    else:
        cursor.execute('INSERT INTO inventory (username, item, count) values (?, ?, ?)', (username, item.name, count))
    con.commit()


def init():
    create_tables()
