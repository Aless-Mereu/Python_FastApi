from __future__ import annotations
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, DateTime, UniqueConstraint, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from .author import AuthorORM
    from .tag import TagORM

# Tabla de asociación para la relación Muchos a Muchos (Many-to-Many) entre Posts y Tags.
# No es una clase ORM completa porque no tiene columnas extra, solo las claves foráneas.
# ondelete="CASCADE": Si borras un post, se borra la relación en esta tabla (limpieza automática).
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


# Definición de la tabla 'posts'
class PostORM(Base):
    __tablename__ = "posts"
    # Restricción a nivel de base de datos: no puede haber dos posts con el mismo título.
    __table_args__ = (UniqueConstraint("title", name="unique_post_title"),)

    # Mapped[...] es la nueva sintaxis de SQLAlchemy 2.0 para definir tipos de forma segura.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Clave foránea (Foreign Key) que apunta a la tabla 'authors'.
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"))
    
    # Relación ORM: Permite acceder a post.author como un objeto Python.
    # back_populates="posts": Sincroniza con la relación inversa en AuthorORM.
    author: Mapped[Optional["AuthorORM"]] = relationship(
        back_populates="posts")

    # Relación Muchos a Muchos con Tags.
    # secondary=post_tags: Indica la tabla intermedia definida arriba.
    # lazy="selectin": Optimización de carga. Carga los tags en una segunda consulta eficiente automáticamente.
    tags: Mapped[List["TagORM"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
        lazy="selectin",
        passive_deletes=True
    )