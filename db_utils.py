import sqlite3
import os
import datetime
import base64

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def ensure_users_table(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = c.fetchone() is not None
    if not table_exists:
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chinese_name TEXT,
            age INTEGER NOT NULL,
            birthday DATE,
            skills TEXT
        )''')
        conn.commit()
    else:
        c.execute("PRAGMA table_info(users)")
        columns = {col[1]: col[2] for col in c.fetchall()}
        if 'chinese_name' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN chinese_name TEXT")
            conn.commit()
        if 'skills' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN skills TEXT")
            conn.commit()
        if 'birthday' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN birthday DATE")
            conn.commit()
        elif columns['birthday'].upper() != 'DATE':
            c.execute('''ALTER TABLE users RENAME TO users_old''')
            c.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                chinese_name TEXT,
                age INTEGER NOT NULL,
                birthday DATE,
                skills TEXT
            )''')
            c.execute('''INSERT INTO users (id, name, chinese_name, age, birthday, skills) SELECT id, name, chinese_name, age, birthday, skills FROM users_old''')
            c.execute('''DROP TABLE users_old''')
            conn.commit()

def add_user(conn, name, chinese_name, age, birthday, skills):
    c = conn.cursor()
    c.execute("INSERT INTO users (name, chinese_name, age, birthday, skills) VALUES (?, ?, ?, ?, ?)", (name, chinese_name, age, birthday, skills))
    conn.commit()

def update_user(conn, user_id, name, chinese_name, age, birthday, skills):
    c = conn.cursor()
    c.execute("UPDATE users SET name=?, chinese_name=?, age=?, birthday=?, skills=? WHERE id=?", (name, chinese_name, age, birthday, skills, user_id))
    conn.commit()

def delete_user(conn, user_id):
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

def get_all_users(conn):
    import pandas as pd
    return pd.read_sql_query("SELECT * FROM users", conn)

def ensure_auth_table(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_auth'")
    if not c.fetchone():
        c.execute('''CREATE TABLE users_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        conn.commit()

def register_user(conn, username, password):
    c = conn.cursor()
    encoded_pw = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    try:
        c.execute("INSERT INTO users_auth (username, password) VALUES (?, ?)", (username, encoded_pw))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already exists."

def check_login(conn, username, password):
    c = conn.cursor()
    encoded_pw = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    c.execute("SELECT id FROM users_auth WHERE username=? AND password=?", (username, encoded_pw))
    row = c.fetchone()
    return row is not None
