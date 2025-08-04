# ✅ FastAPI endpoints для загрузки и редактирования dresscode стандартов
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RULES_FILE = "rules.json"

@app.get("/api/rules")
async def get_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    return JSONResponse(content=data)

@app.post("/api/rules/update")
async def update_rules(request: Request):
    data = await request.json()
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "updated"}
