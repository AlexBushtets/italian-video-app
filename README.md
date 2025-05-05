# Italian Video Generator 🇮🇹🎬

Веб-сервис для генерации обучающих видео по итальянским словам, глаголам и фразам.

## Возможности

- Выбор категории: глаголы, существительные или фразы
- Задание времени показа каждой фразы (в секундах)
- Формат генерации: 
  - 🎞️ Видео с озвучкой
  - 🎬 Видео без озвучки
  - 🔊 Только аудио
- Порядок слов: частотный или случайный
- Асинхронная генерация с индикатором прогресса

## Технологии

- Backend: Python, FastAPI
- Frontend: HTML, JS (Vanilla)
- Генерация видео: OpenCV, PIL, TTS

## Запуск

```bash
# Клонируем репозиторий
git clone https://github.com/AlexBushtets/italian-video-app.git
cd italian-video-app

# Создаём виртуальное окружение и активируем его
python -m venv venv
venv\Scripts\activate  # для Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Запуск сервера
uvicorn backend.app.main:app --reload
