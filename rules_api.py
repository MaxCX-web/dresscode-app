"""
REST‑API для чтения и обновления стандартов дресс‑кода.
Позволяет получать актуальные рекомендации из файла `rules.json` и
обновлять их посредством POST‑запроса.
"""

import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Разрешаем кросс‑доменные запросы, чтобы API можно было
# вызывать из браузера на любом домене.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Имя файла с правилами
RULES_FILE = "rules.json"


@app.get("/api/rules")
async def get_rules() -> JSONResponse:
    """Возвращает содержимое файла с правилами.

    Returns:
        JSONResponse: JSON‑объект с полем `tips` и `lastUpdated`.
    """
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    return JSONResponse(content=data)


@app.post("/api/rules/update")
async def update_rules(request: Request) -> JSONResponse:
    """
    Принимает JSON с новыми правилами и сохраняет его в файл.

    Args:
        request (Request): запрос, содержащий JSON

    Returns:
        JSONResponse: статус обновления
    """
    data = await request.json()
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return JSONResponse(content={"status": "updated"})