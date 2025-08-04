# ✅ FastAPI backend для проверки дресс‑кода с инференсом модели
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import uuid
import os
from predict import predict_image
from sqlite_logger import log_submission
import download_model  # автоматически загрузит модель при запуске


app = FastAPI()

# Разрешаем любые источники (origins) и методы для взаимодействия с API,
# поскольку приложение может использоваться из браузера или других клиентов.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Директория, куда будут сохраняться загруженные изображения.  
# При запуске приложения создаём её, если такой папки ещё нет.
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/check")
async def check_dresscode(
    file: UploadFile = File(...),
    email: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
):
    """
    Принимает изображение и информацию о пользователе, сохраняет файл на диск
    и возвращает результат проверки дресс‑кода.

    Args:
        file (UploadFile): загружаемое изображение
        email (str): e‑mail отправителя
        name (str): имя отправителя
        surname (str): фамилия отправителя

    Returns:
        JSONResponse: объект с результатом (`"OK"` или `"FAIL"`).
    """
    # Формируем уникальное имя файла для сохранения
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    # Сохраняем содержимое загруженного файла на диск
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Выполняем инференс модели по сохранённому изображению
    result = predict_image(filepath)
    # Логируем обращение в базу данных
    log_submission(email, name, surname, filename, result)

    # Возвращаем результат клиенту
    return JSONResponse(content={"result": result})