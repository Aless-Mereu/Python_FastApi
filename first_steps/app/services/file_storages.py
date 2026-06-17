import os
import shutil
from uuid import uuid4
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File


MEDIA_DIR = "app/media"  # Carpeta donde se guardarán los archivos subidos
ALLOW_MIME = ["image/jpeg", "image/png"]  # Tipos de archivos permitidos


def endure_media_dir() -> None:
    """Crea la carpeta media si no existe."""
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    
    
def save_upload_image(file: UploadFile) -> dict:
    if file.content_type not in ALLOW_MIME:
        raise HTTPException(
            status_code=400, 
            detail="Solo se permiten imágenes JPEG y PNG.")
        
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