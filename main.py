from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import os

app = FastAPI()

# http://127.0.0.1:8011/docs (Swagger UI)
# http://127.0.0.1:8011/redoc (ReDoc)

# запуск: uvicorn main:app --reload --host 127.0.0.1 --port 8011
# http://127.0.0.1:8011/get_id
@app.get("/get_id")
async def get_unique_id() -> Dict[str, Any]:
    import uuid
    unique_id = str(uuid.uuid4())
    return {"id": unique_id}

# http://127.0.0.1:8011/get_file
@app.get("/get_file")
async def get_text_file():
    file_path = "example.txt"
    return FileResponse(file_path, media_type="text/plain")

# http://127.0.0.1:8011/download_binary
@app.get("/download_binary")
async def download_binary_file():
    file_path = "test_image.jpg"  # Замените на путь к вашему файлу
    
    # Проверка, существует ли файл
    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404
    
    # Открываем файл для чтения в бинарном режиме
    file_like_object = open(file_path, mode="rb")
    
    # Определяем тип содержимого для бинарных данных
    media_type = "application/octet-stream"
    
    return StreamingResponse(file_like_object, media_type=media_type)