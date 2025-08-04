# ✅ Инференс обученной модели дресс-кода (predict.py)
import torch
from torchvision import transforms, models
from PIL import Image
import os

MODEL_PATH = 'dresscode_model.pt'
LABELS = ['FAIL', 'OK']  # Порядок должен совпадать с ImageFolder

# Преобразования как при обучении
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_model():
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
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
