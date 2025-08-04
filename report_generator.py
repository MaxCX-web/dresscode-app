"""
Модуль для генерации PDF‑отчёта на основе данных из базы SQLite.
Извлекает все записи из таблицы `submissions` и формирует отчёт,
который можно сохранить в файл.
"""

import sqlite3
from fpdf import FPDF
import datetime

# Имя файла базы данных с результатами
DB_FILE = "submissions.db"


class PDF(FPDF):
    """Класс для настройки заголовка и подвала PDF‑документа."""

    def header(self) -> None:
        # Заголовок
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Отчёт по проверке дресс‑кода", ln=True, align="C")

    def footer(self) -> None:
        # Номер страницы внизу
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Страница {self.page_no()}", align="C")


def generate_report(filename: str = "report.pdf") -> None:
    """
    Собирает все записи из базы и создаёт PDF‑документ.

    Args:
        filename (str): имя файла, куда будет сохранён отчёт
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        SELECT timestamp, email, name, surname, filename, result
        FROM submissions
        ORDER BY timestamp DESC
        """
    )
    rows = c.fetchall()
    conn.close()

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for row in rows:
        timestamp, email, name, surname, fname, result = row
        line = f"{timestamp} | {name} {surname} | {email} | Результат: {result} | Файл: {fname}"
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    print(f"✅ PDF отчёт сохранён: {filename}")


if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    generate_report(f"report_{today}.pdf")