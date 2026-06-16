import os
import shutil
from uuid import uuid4
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File


MEDIA_DIR = "app/media"  # Carpeta donde se guardarán los archivos subidos

router = APIRouter(prefix="/upload", tags=["uploads"])
@router.post("/bytes")
async def upload_bytes(file: bytes = File(...)):# File(...) indica que este campo es obligatorio y se espera un archivo.
    return{
        "filename": "archivo subido",
        "size": len(file)
    }



@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    return{
        "filename": file.filename,
        "content-type": file.content_type
    }
    
    
@router.post("/save")
async def save_file(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Solo se permiten imágenes JPEG y PNG.")
        
    ext = os.path.splitext(file.filename)[1]  # Obtiene la extensión del archivo (.ej. .jpg, .png)
    filename = f"{uuid.uuid4().hex}{ext}"  # Genera un nombre único para el archivo
    file_path = os.path.join(MEDIA_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # Guarda el archivo en la carpeta media
        return {
            "filename": filename,
            "content-type": file.content_type,
            "url": f"/media/{filename}"  # URL para acceder al archivo subido
        }