# ✅ Скачивает модель dresscode_model.pt из публичной ссылки
import requests

MODEL_URL = "https://drive.google.com/uc?export=download&id=12BCn9rwR6_DQltSNdRQgA-LoesALXRoR"  # ⚠️ ← замени на свою ссылку
MODEL_PATH = "dresscode_model.pt"

def download_model():
    response = requests.get(MODEL_URL, stream=True)
    response.raise_for_status()
    with open(MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Модель успешно загружена!")

if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        download_model()
    else:
        print("✅ Модель уже загружена.")
