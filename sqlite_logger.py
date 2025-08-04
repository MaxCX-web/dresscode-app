"""
Модуль для логирования результатов проверки дресс‑кода в локальную базу SQLite.
При импортировании создаёт таблицу `submissions`, если она отсутствует, и
предоставляет функцию для добавления записей.
"""

import sqlite3
import datetime

# Имя файла базы данных
DB_FILE = "submissions.db"


def init_db() -> None:
    """Создаёт таблицу submissions, если она ещё не существует."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            email TEXT,
            name TEXT,
            surname TEXT,
            filename TEXT,
            result TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def log_submission(email: str, name: str, surname: str, filename: str, result: str) -> None:
    """
    Добавляет новую запись о проверке в таблицу `submissions`.

    Args:
        email (str): e‑mail пользователя
        name (str): имя пользователя
        surname (str): фамилия пользователя
        filename (str): имя сохранённого файла изображения
        result (str): результат инференса ('OK' или 'FAIL')
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute(
        """
        INSERT INTO submissions (timestamp, email, name, surname, filename, result)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (timestamp, email, name, surname, filename, result),
    )
    conn.commit()
    conn.close()


# Инициализируем базу данных при импорте модуля
init_db()