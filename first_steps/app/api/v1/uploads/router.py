import os
import shutil
from uuid import uuid4
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.file_storages import save_upload_image, endure_media_dir


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
    saved = await save_upload_image(file)
    
    return {
            "filename": saved["filename"],
            "content-type": saved["content-type"],
            "url": saved["url"]
        }