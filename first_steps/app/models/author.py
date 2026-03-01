# __future__.annotations: Permite usar tipos que aún no se han definido completamente.
# Es útil para que Python no se queje si usamos "PostORM" antes de que se lea ese archivo.
from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

# TYPE_CHECKING es True solo cuando herramientas como MyPy revisan el código, pero False cuando el programa corre.
# Esto evita el error de "Importación Circular" (Author importa Post, y Post importa Author).
if TYPE_CHECKING:
    from .post import PostORM


# Modelo ORM para la tabla de Autores.
class AuthorORM(Base):
    __tablename__ = "authors"

    # Mapped[int]: Define el tipo de dato en Python.
    # mapped_column(...): Define la configuración en la base de datos (SQL).
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # nullable=False: Este campo es obligatorio en la base de datos (NOT NULL).
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # unique=True: No puede haber dos autores con el mismo email.
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Relación Uno a Muchos (One-to-Many): Un autor puede tener muchos posts.
    # back_populates="author": Conecta con la propiedad 'author' en la clase PostORM.
    posts: Mapped[List["PostORM"]] = relationship(back_populates="author")