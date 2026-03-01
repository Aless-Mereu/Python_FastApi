from fastapi import FastAPI
from app.core.db import Base, engine
from dotenv import load_dotenv
from app.api.v1.post.router import router as post_router
# Si el archivo auth/router.py no existe, comenta la siguiente línea:
from app.api.v1.auth.router import router as auth_router

load_dotenv()


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

    return app


app = create_app()

