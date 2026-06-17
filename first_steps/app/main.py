import os
from fastapi import FastAPI
from app.core.db import Base, engine
from dotenv import load_dotenv
from app.api.v1.post.router import router as post_router
# Si el archivo auth/router.py no existe, comenta la siguiente línea:
from app.api.v1.auth.router import router as auth_router
from app.api.v1.uploads.router import router as uploads_router
from fastapi.staticfiles import StaticFiles

load_dotenv()

MEDIA_DIR = "app/media"  # Carpeta donde se guardarán los archivos subidos


def create_app() -> FastAPI:
    app = FastAPI(title="Mini Blog")
    
    # Crea las tablas en la base de datos si no existen.
    # NOTA: En producción, esto se suele reemplazar por migraciones con Alembic.
    Base.metadata.create_all(bind=engine)

    # Registra las rutas definidas en el router de posts
    app.include_router(post_router)
    # Registra las rutas definidas en el router de autenticación
    # Si auth_router no está definido, comenta la siguiente línea:
    app.include_router(auth_router, prefix="/api/v1")
    
    app.include_router(uploads_router)

    os.makedirs(MEDIA_DIR, exist_ok=True)  # Crea la carpeta media si no existe
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")  # Monta la carpeta media para servir archivos estáticos

    return app


app = create_app()

