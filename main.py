from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import Response, FileResponse, StreamingResponse
from typing import Dict, Any
import os
import uuid
from pydantic import BaseModel
import base64

app = FastAPI()

# http://127.0.0.1:8011/docs (Swagger UI)
# http://127.0.0.1:8011/redoc (ReDoc)

# запуск: uvicorn main:app --reload --host 0.0.0.0 --port 8011
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

# http://127.0.0.1:8011/sign-xml
class SignRequest(BaseModel):
    data: str

@app.post("/sign-xml/", summary="Подписать XML файл")
async def sign_xml(request: SignRequest = Body(...)):
    try:
        # Декодируем base64 строку
        # Убираем возможные пробелы и переносы строк
        clean_base64 = request.data.strip().replace('\n', '').replace('\r', '').replace(' ', '')
        xml_content = base64.b64decode(clean_base64)
        
        # Логика подписи XML
        signed_content = xml_content
        
        # Возвращаем подпись как бинарный файл
        return Response(
            content=signed_content,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": "attachment; filename=document.sgn",
            }
        )
        
    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Некорректная base64 строка")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")