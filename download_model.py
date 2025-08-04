"""
Утилита для загрузки модели dresscode из публичной ссылки Google Drive.
Если файл модели уже существует, скачивание не выполняется.
"""

import os
import requests

# Публичная ссылка на весовой файл модели
MODEL_URL = (
    "https://drive.google.com/uc?export=download&id=12BCn9rwR6_DQltSNdRQgA-LoesALXRoR"
)
# Имя файла, куда будет сохранён скачанный вес
MODEL_PATH = "dresscode_model.pt"


def download_model() -> None:
    """Скачивает модель по ссылке `MODEL_URL` и сохраняет в `MODEL_PATH`."""
    print("⬇️ Начинаем загрузку модели...")
    response = requests.get(MODEL_URL, stream=True)
    response.raise_for_status()
    with open(MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("✅ Модель успешно загружена!")


if __name__ == "__main__":
    # Если модель отсутствует, скачиваем её
    if not os.path.exists(MODEL_PATH):
        download_model()
    else:
        print("✅ Модель уже загружена.")