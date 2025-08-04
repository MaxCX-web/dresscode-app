"""
Скрипт для обучения модели дресс‑кода на наборе изображений.
Использует PyTorch и torchvision для загрузки данных и обучения модели
на основе предобученной ResNet‑18. Параметры обучения (batch size,
число эпох и т.д.) можно скорректировать в начале файла.
"""

import os
import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

# Параметры обучения
BATCH_SIZE = 16
EPOCHS = 5
DATA_DIR = "dataset"
MODEL_PATH = "dresscode_model.pt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(EPOCHS):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, preds = outputs.max(1)
        total += labels.size(0)
        correct += preds.eq(labels).sum().item()

    print(
        f"Epoch {epoch + 1}: Loss={total_loss:.4f}, Accuracy={correct / total:.2%}"
    )

torch.save(model.state_dict(), MODEL_PATH)
print(f"✅ Модель сохранена: {MODEL_PATH}")