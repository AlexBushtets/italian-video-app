from fastapi import FastAPI
from .api import router
from fastapi.staticfiles import StaticFiles
import os

# Абсолютный путь к frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

# Абсолютный путь к папке с видео
videos_path = os.path.join(os.path.dirname(__file__), "..", "..", "videos")

# Создаём FastAPI-приложение
app = FastAPI(
    title="Italian Video Generator",
    description="Создание обучающих видео по итальянским словам",
    version="1.0.0"
)

# Подключаем маршруты
app.include_router(router)

# Монтируем папку с видео
app.mount("/download", StaticFiles(directory=videos_path), name="videos")

# Монтируем HTML-фронтенд
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Для отладки
if __name__ == "__main__":
    print("APP IS DEFINED:", app)

