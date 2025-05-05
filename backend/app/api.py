from fastapi import APIRouter, Form, Response
from fastapi.responses import JSONResponse, FileResponse
from threading import Thread
from .video_generator import generate_video
import os
import uuid

router = APIRouter()

# Фоновая задача генерации видео
def background_task(category: str, count: int, delay: int, order: str, format: str, output_path: str):
    generate_video(category, count, delay, order, format, output_path)
    # Удаляем .lock-файл после завершения генерации
    lock_path = output_path + ".lock"
    if os.path.exists(lock_path):
        os.remove(lock_path)

@router.post("/generate-video")
def generate_video_endpoint(
    category: str = Form(...),
    count: int = Form(...),
    delay: int = Form(3),
    order: str = Form("shuffle"),
    format: str = Form("video_audio")
):
    uid = str(uuid.uuid4())[:8]
    filename = f"{category}_{count}_{delay}s_{order}_{format}_{uid}.mp4"
    output_path = f"videos/{filename}"
    lock_path = output_path + ".lock"

    # Создаём .lock-файл как индикатор того, что видео ещё пишется
    with open(lock_path, "w") as f:
        f.write("processing")

    # Запуск фоновой генерации
    thread = Thread(target=background_task, args=(category, count, delay, order, format, output_path))
    thread.start()

    return JSONResponse({
        "status": "видео создаётся",
        "file": filename,
        "download_url": f"/download/{filename}"
    })

@router.get("/download/{filename}")
def download_video(filename: str):
    filepath = f"videos/{filename}"
    lock_path = filepath + ".lock"
    if os.path.exists(filepath) and not os.path.exists(lock_path):
        return FileResponse(filepath, media_type="video/mp4", filename=filename)
    return JSONResponse({"error": "Файл ещё не готов"}, status_code=404)

@router.head("/download/{filename}")
def check_video_ready(filename: str):
    filepath = f"videos/{filename}"
    lock_path = filepath + ".lock"
    if os.path.exists(filepath) and not os.path.exists(lock_path):
        return Response(status_code=200)
    return Response(status_code=404)

@router.get("/check-file/{filename}")
def check_file_exists(filename: str):
    filepath = f"videos/{filename}"
    lock_path = filepath + ".lock"
    if os.path.exists(filepath) and not os.path.exists(lock_path):
        return JSONResponse({"ready": True})
    return JSONResponse({"ready": False}, status_code=404)


