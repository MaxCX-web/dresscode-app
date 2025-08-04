# ✅ FastAPI backend для проверки дресс-кода с инференсом модели
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/check")
async def check_dresscode(
    file: UploadFile = File(...),
    email: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...)
):
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_image(filepath)
    log_submission(email, name, surname, filename, result)

    return JSONResponse(content={"result": result})
