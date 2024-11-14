import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birthdate TEXT,
            city TEXT,
            gender TEXT,
            instagram TEXT,
            onlyfans TEXT,
            twitter TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_data(name, birthdate, city, gender, instagram, onlyfans, twitter):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, birthdate, city, gender, instagram, onlyfans, twitter)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, birthdate, city, gender, instagram, onlyfans, twitter))
    conn.commit()
    conn.close()