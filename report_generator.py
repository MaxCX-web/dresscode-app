# ✅ Генерация PDF-отчёта из базы результатов
import sqlite3
from fpdf import FPDF
import datetime

DB_FILE = 'submissions.db'

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Отчёт по проверке дресс-кода', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Страница {self.page_no()}', align='C')

def generate_report(filename='report.pdf'):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT timestamp, email, name, surname, filename, result FROM submissions ORDER BY timestamp DESC')
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

if __name__ == '__main__':
    today = datetime.date.today().isoformat()
    generate_report(f'report_{today}.pdf')
