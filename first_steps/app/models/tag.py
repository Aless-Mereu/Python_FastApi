from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

# Importación condicional para evitar ciclos (Tag <-> Post)
if TYPE_CHECKING:
    from .post import PostORM


# Modelo ORM para la tabla de Etiquetas (Tags).
class TagORM(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # unique=True: Evita duplicados como "Python" y "Python" en la tabla de tags.
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    # Relación Muchos a Muchos (Many-to-Many) con Posts.
    # secondary="post_tags": Le dice a SQLAlchemy que use la tabla intermedia 'post_tags' 
    # para encontrar qué posts tienen esta etiqueta.
    posts: Mapped[List["PostORM"]] = relationship(
        secondary="post_tags",
        back_populates="tags",
        # lazy="selectin": Estrategia de carga. Cuando pidas un Tag, SQLAlchemy hará 
        # una segunda consulta rápida para traer todos sus posts automáticamente.
        lazy="selectin"
    )