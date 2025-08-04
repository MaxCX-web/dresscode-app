# ✅ Логирование результатов проверок в SQLite
import sqlite3
import datetime

DB_FILE = 'submissions.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            email TEXT,
            name TEXT,
            surname TEXT,
            filename TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_submission(email, name, surname, filename, result):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO submissions (timestamp, email, name, surname, filename, result)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, email, name, surname, filename, result))
    conn.commit()
    conn.close()

# Инициализируем БД при импорте
init_db()
