import sqlite3


def create_tables():
    """Создание таблиц users и items"""
    with sqlite3.connect('users.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY_KEY,
            user VARCHAR(50),
            username VARCHAR(50),
            balance INT,
            accept BIN
        )""")
        db.commit()

    with sqlite3.connect('items.db') as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS items (
            item_id INT PRIMARY_KEY,
            name VARCHAR(50),
            description VARCHAR(300),
            price INT,
            url VARCHAR(500)
        )""")
        db.commit()
    print('Таблицы созданы.')


def check_or_add_user(user_id, user, username, balance, accept):
    """Добавление пользователя в таблицу users.db, если его там нет"""
    with sqlite3.connect('users.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        if cursor.fetchone() is None:
            add_user(user_id, user, username, balance, accept)
            print('Новый пользователь: ' + user)
        else:
            print('Существующий пользователь: ' + user)


def add_user(user_id, user, username, balance=0, accept=0):
    """Добавление пользователя в таблицу users.db"""
    with sqlite3.connect('users.db', check_same_thread=False) as db:
        cursor = db.cursor()
        values = user_id, user, username, balance, accept
        cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?)", values)
        db.commit()


def is_accept(user_id):
    """Проверка пользователя на подтверждение соглашения"""
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        return [x for x in cursor.execute(f"SELECT accept FROM users WHERE user_id = {user_id}")][0][0]


def accept_user(user_id):
    """Принятие соглашение в таблице"""
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET accept = 1 WHERE user_id = {user_id}")
        db.commit()


def send_profile_data(message):
    """Отправление данных о пользователе: айди, имя, баланс"""
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        return [x for x in cursor.execute("SELECT user_id, user, balance FROM users "
                                          f"WHERE user_id = {message.from_user.id}")]


def add_balance(user_id, amount):
    """Пополнение баланса в боте через базу данных"""
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        balance = [x for x in cursor.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")][0][0]
        cursor.execute(f"UPDATE users SET balance = {balance + amount} WHERE user_id = {user_id}")
        db.commit()


def count_rows():
    """Подсчитывает общее количество строк в базе данных"""
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        return [x for x in cursor.execute("SELECT COUNT(*) FROM users")][0][0]


def count_balance():
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        return [x for x in cursor.execute("SELECT SUM(balance) FROM users WHERE balance > 0")][0][0]


count = 1


def add_item(name, description, price, url):
    global count
    with sqlite3.connect('items.db') as db:
        cursor = db.cursor()
        values = (count, name, description, price, url)
        cursor.execute("INSERT INTO items VALUES(?, ?, ?, ?, ?)", values)
        db.commit()
        count += 1
