import sqlite3
from config import knownUsers, userStep, dtd


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_con():
    mydb = sqlite3.connect(f'db.sqlite')
    mydb.row_factory = dict_factory
    return mydb


def init():
    mydb = db_con()
    cursor = mydb.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         chat_id BIGINT,
                         first_name TEXT,
                         username TEXT,
                         last_name TEXT,
                         language_code TEXT,
                         is_premium BOOL DEFAULT 0,
                         reflink TEXT,
                         status INT DEFAULT 1,
                         reg_data DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS tokens (
                         id INTEGER PRIMARY KEY,
                         name VARCHAR(30),
                         price_api VARCHAR(512),
                         price_keys VARCHAR(512),
                         explorer_api VARCHAR(512),
                         explorer_keys VARCHAR(512),
                         units INT,
                         add_chat_id INT,
                         price FLOAT DEFAULT 0,
                         status BOOL DEFAULT 1,
                         add_data DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS token_prices (
                         id INTEGER PRIMARY KEY,
                         token_id INT,
                         price FLOAT,
                         add_data DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS user_tokens (
                         id INTEGER PRIMARY KEY,
                         chat_id BIGINT, 
                         token_name TEXT,
                         available_balance FLOAT DEFAULT 0,
                         staked_balance FLOAT DEFAULT 0,
                         unstaked_balance FLOAT DEFAULT 0,
                         rewards_balance FLOAT DEFAULT 0,
                         watch_address VARCHAR(100),
                         status BOOL DEFAULT 1,
                         add_data DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()

    for usr in users:
        knownUsers[usr['chat_id']] = usr['status']
        userStep[usr['chat_id']] = 'MAIN_MENU'
        dtd[usr['chat_id']] = {}


# =======tokens=======
def update_token_price(token_id, price):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE tokens SET price = ? WHERE id = ?", (price, token_id))
    mydb.commit()
    cursor.close()


def get_tokens():
    cursor = db_con().cursor()
    cursor.execute("SELECT * FROM tokens WHERE status = 1")
    result = cursor.fetchall()
    cursor.close()
    return result


def get_token_by_id(token_id):
    cursor = db_con().cursor()
    cursor.execute("SELECT * FROM tokens WHERE id = ?", (token_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


def get_user_token_by_id(token_id):
    cursor = db_con().cursor()
    cursor.execute("SELECT * FROM user_tokens WHERE id = ?", (token_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


def add_token(chat_id, name, price_api, price_keys, explorer_api, explorer_keys, units):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO tokens (add_chat_id, name, price_api, price_keys, explorer_api, explorer_keys, units)
        VALUES (?,?,?,?,?,?,?)""", (chat_id, name, price_api, price_keys, explorer_api, explorer_keys, units))
    mydb.commit()
    result = cursor.lastrowid
    cursor.close()
    return result


def get_user_tokens(cid=None):
    cursor = db_con().cursor()

    if cid is None:
        cursor.execute("SELECT * FROM user_tokens")
        result = cursor.fetchall()

    else:
        cursor.execute("SELECT * FROM user_tokens WHERE chat_id = ? and status = 1", (cid, ))
        result = cursor.fetchall()

    cursor.close()
    return result


def delete_user_token(user_token_id):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE user_tokens SET status = 0 WHERE id = ?", (user_token_id, ))
    mydb.commit()
    cursor.close()


def add_user_token(chat_id, token_name, available_balance=None, watch_address=None):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO user_tokens (chat_id, token_name, available_balance, watch_address)
        VALUES (?,?,?,?)""", (chat_id, token_name, available_balance, watch_address))
    mydb.commit()
    result = cursor.lastrowid
    cursor.close()
    return result


# =======users=======
def get_user_by_username(username):
    cursor = db_con().cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result


def add_user(chat_id, first_name, username, last_name, language_code, reflink, is_premium):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO users (chat_id, first_name, username, last_name, language_code, reflink, is_premium)
        VALUES (?,?,?,?,?,?,?)""", (chat_id, first_name, username, last_name, language_code, reflink, is_premium))
    mydb.commit()
    result = cursor.lastrowid
    cursor.close()
    return result


def update_user_status(chat_id, status):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE users SET status = ? WHERE chat_id = ?", (status, chat_id))
    mydb.commit()
    cursor.close()


def get_user(chat_id):
    cursor = db_con().cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    return cursor.fetchone()


def update_user_token_balance(user_token_id, balance):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE user_tokens SET available_balance = ? WHERE id = ?", (balance, user_token_id))
    mydb.commit()
    cursor.close()


def update_user_token_stake_balance(user_token_id, balance):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE user_tokens SET staked_balance = ? WHERE id = ?", (balance, user_token_id))
    mydb.commit()
    cursor.close()


def update_user_token_rewards_balance(user_token_id, balance):
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE user_tokens SET rewards_balance = ? WHERE id = ?", (balance, user_token_id))
    mydb.commit()
    cursor.close()
