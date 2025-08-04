import os
import torch
import requests
from PIL import Image
from torchvision import transforms, models

MODEL_PATH = "dresscode_model.pt"
MODEL_URL = "https://drive.google.com/uc?export=download&id=12BCn9rwR6_DQltSNdRQgA-LoesALXRoR"  # замените на прямую ссылку

LABELS = ['FAIL', 'OK']

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("⬇️ Скачиваем модель dresscode_model.pt ...")
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)
        print("✅ Модель успешно загружена")

download_model()

def load_model():
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    model = torch.load(MODEL_PATH, map_location='cpu')
model.eval()

    model.eval()
    return model

model = load_model()

def predict_image(image_path: str) -> str:
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = outputs.max(1)
        return LABELS[predicted.item()]
