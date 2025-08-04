"""
Модуль для загрузки модели и предсказания принадлежности изображения
к допустимому дресс‑коду. При первом импорте скачивает модель с Google Drive
и сохраняет её в локальный файл `dresscode_model.pt`.

Использует PyTorch и torchvision для построения нейросетевой модели на
основе ResNet‑18 и преобразования входных изображений.
"""

import os
import requests
from PIL import Image

try:
    import torch  # type: ignore
    from torchvision import transforms, models  # type: ignore
except ModuleNotFoundError:
    # Если нет библиотеки torch/torchvision, определим заглушку
    torch = None  # type: ignore
    transforms = None  # type: ignore
    models = None  # type: ignore

# Путь к локальному файлу модели
MODEL_PATH = "dresscode_model.pt"
# Ссылка на модель в Google Drive; при необходимости замените на прямую
MODEL_URL = (
    "https://drive.google.com/uc?export=download&id=12BCn9rwR6_DQltSNdRQgA-LoesALXRoR"
)

# Метки классов, возвращаемые моделью
LABELS = ["FAIL", "OK"]

# Последовательность преобразований, применяемая к входному изображению
if transforms is not None:
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
else:
    transform = None  # type: ignore


def download_model() -> None:
    """Скачивает модель из облака, если локального файла ещё нет.

    Если зависимости torch/torchvision отсутствуют, пропускает загрузку,
    поскольку модель всё равно не сможет быть использована.
    """
    if torch is None:
        # Нет поддержки torch, пропускаем скачивание
        return
    if not os.path.exists(MODEL_PATH):
        print("⬇️ Скачиваем модель dresscode_model.pt ...")
        response = requests.get(MODEL_URL)
        response.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Модель успешно загружена")


def load_model():
    """
    Загружает модель из файла и возвращает её. Если зависимостей нет,
    возвращает None, что означает, что будет использоваться заглушка.
    """
    if torch is None or models is None:
        return None
    # Создаём базовую архитектуру ResNet18 без предобученных весов
    model = models.resnet18(pretrained=False)
    # Заменяем последний полносвязный слой под нашу задачу из 2 классов
    model.fc = torch.nn.Linear(model.fc.in_features, len(LABELS))
    # Загружаем веса модели
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model


# При импорте модуля сразу скачиваем и загружаем модель (если возможно)
download_model()
model = load_model()


def predict_image(image_path: str) -> str:
    """
    Выполняет инференс модели по указанному изображению и возвращает
    строку с названием предсказанного класса. Если модель недоступна,
    возвращает фиктивный результат 'OK'.

    Args:
        image_path (str): путь к файлу изображения

    Returns:
        str: 'OK' или 'FAIL'
    """
    # Если модель недоступна, возвращаем фиктивный ответ
    if model is None or torch is None or transform is None:
        return "OK"
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = outputs.max(1)
    return LABELS[predicted.item()]