# 👔 DSINV Dresscode AI — Проверка внешнего вида сотрудников

## 📦 Структура проекта

```
dresscode_project/
├── main.py               # FastAPI сервер для проверки фото
├── predict.py            # AI-классификация (дресс-код)
├── train.py              # Обучение модели на фото
├── rules_api.py          # API для редактирования dresscode правил
├── sqlite_logger.py      # Логирование результатов в SQLite
├── report_generator.py   # Генерация PDF-отчётов
├── rules.json            # Правила дресс-кода (редактируемые)
├── dresscode_model.pt    # Готовая обученная модель
├── requirements.txt      # Зависимости
├── dataset/              # Фото для обучения
│   ├── OK/
│   └── FAIL/
├── uploads/              # Загрузка фото пользователей
```

---

## 🚀 Быстрый старт

### 1. Установи зависимости

```bash
pip install -r requirements.txt
```

### 2. Обучи модель (если ещё нет)

Положи фото в `dataset/OK/` и `dataset/FAIL/`, затем:

```bash
python train.py
```

> В результате появится `dresscode_model.pt`

### 3. Запусти backend-сервер

```bash
python main.py
```

> Сервер поднимется на `http://localhost:8000`

---

## 🔍 Функциональность

- 📤 Загрузка фото через веб-интерфейс
- 🤖 AI-модель проверяет соответствие дресс-коду
- 👨‍💼 Админка: редактирование dresscode стандартов
- 🗂 Логирование всех проверок в SQLite
- 🧾 Генерация PDF-отчётов для руководства

---

## 📄 Отчёты

Сформируй PDF:

```bash
python report_generator.py
```

Получишь файл `report_YYYY-MM-DD.pdf` в корне проекта.

---

## ☁️ Планы на деплой

Бэкенд можно выложить на:
- [Render.com](https://render.com/) (FastAPI поддерживается нативно)

Фронтенд на:
- [Vercel](https://vercel.com/) или [Netlify](https://netlify.com/)

---

## 📧 Авторизация

Авторизация по email домена `@dsinv.ru`. Администратор — `admin@dsinv.ru`

---

## 🧠 Контакты разработчика

