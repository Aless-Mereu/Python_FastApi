import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session,DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db #no se pone return ya que terminaría la función. Con yield(Expresión generadora) hace una pausa y cuando el endpoint lo termine de usar entonces entra finally.
    finally:
        db.close()