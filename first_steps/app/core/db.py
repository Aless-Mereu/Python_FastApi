import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session,DeclarativeBase

# Obtiene la URL de la base de datos de las variables de entorno.
# Si no existe, usa SQLite por defecto (crea un archivo blog.db local).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine_kwargs = {}

# Configuración específica para SQLite:
# SQLite por defecto no permite compartir conexiones entre hilos (threads).
# FastAPI usa múltiples hilos, así que 'check_same_thread': False es necesario para evitar errores.
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

# create_engine: Establece la conexión física con la base de datos.
# echo=True: Imprime las consultas SQL en la consola (útil para depurar).
# pool_pre_ping=True: Verifica que la conexión esté viva antes de usarla.
engine = create_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True, **engine_kwargs)

# sessionmaker: Es una "fábrica" de sesiones.
# Una sesión es el "manejador" que usaremos para hablar con la BD en cada petición.
# autocommit=False: Queremos controlar manualmente cuándo guardar (commit) para manejar transacciones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


# Base: Clase padre de la que heredarán todos nuestros modelos (tablas).
# Esto permite a SQLAlchemy saber qué clases son tablas de base de datos.
class Base(DeclarativeBase):
    pass


# get_db: Esta función es una Dependencia de FastAPI.
# Se ejecuta en cada petición (request) que necesite base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db #no se pone return ya que terminaría la función. Con yield(Expresión generadora) hace una pausa y cuando el endpoint lo termine de usar entonces entra finally.
    finally:
        db.close()