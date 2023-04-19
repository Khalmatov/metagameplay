import sqlite3
from typing import List, Any

from dto import Item, UserItem


con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()


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


def get_all_usernames() -> list[str]:
    res = cursor.execute('SELECT username FROM users')
    return [i[0] for i in res.fetchall()]


def is_user_exists(username: str) -> bool:
    res = cursor.execute('SELECT username FROM users WHERE username=?', (username,))
    return res.fetchone()


def create_credits_of_user(username: str):
    cursor.execute('INSERT INTO credits(username, balance) values (?, 0)', (username,))
    con.commit()


def add_credits_to_user(username: str, count: int):
    cursor.execute('UPDATE credits SET balance = balance + ? WHERE username = ?', (count, username))
    con.commit()


def get_user_balance(username: str) -> int:
    res = cursor.execute('SELECT balance FROM credits WHERE username=?', (username,))
    return res.fetchone()[0]


def get_user_items(username: str) -> list[UserItem]:
    res = cursor.execute('''
        SELECT inventory.item, inventory.count, items.price
            FROM inventory
            JOIN items
                ON inventory.item = items.name
            WHERE username=?
    ''', (username,))
    return [UserItem(name=item[0], count=item[1], price=item[2]) for item in res.fetchall()]


def get_all_items() -> list[Item]:
    res = cursor.execute('SELECT name, price FROM items')
    return [Item(name=item[0], price=item[1]) for item in res.fetchall()]


def get_item(item_name: str) -> Item:
    resp = cursor.execute('SELECT name, price FROM items WHERE name=?', (item_name,))
    name, price = resp.fetchone()
    return Item(name=name, price=price)


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
