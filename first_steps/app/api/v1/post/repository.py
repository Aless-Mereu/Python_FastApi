
from math import ceil
from typing import Optional, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload
from app.models import PostORM, AuthorORM, TagORM


# Patrón Repositorio: Abstrae la lógica de base de datos del Router (API).
# El Router solo pide "dame posts", el Repositorio sabe "cómo hacer el SELECT".
class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, post_id: int) -> Optional[PostORM]:
        # Construye la consulta SELECT * FROM posts WHERE id = post_id
        post_find = select(PostORM).where(PostORM.id == post_id)
        # Ejecuta y devuelve un solo objeto o None si no existe.
        return self.db.execute(post_find).scalar_one_or_none()

    # Función compleja para buscar, filtrar y paginar.
    # Devuelve una tupla: (total de items encontrados, lista de items en la página actual)
    def search(
            self,
            query: Optional[str],
            order_by: str,
            direction: str,
            page: int,
            per_page: int
    ) -> Tuple[int, List[PostORM]]:

        # 1. Inicia la consulta base
        results = select(PostORM)

        # 2. Aplica filtro de búsqueda si existe 'query'
        if query:
            # ilike: Case-insensitive LIKE (busca mayúsculas y minúsculas)
            results = results.where(PostORM.title.ilike(f"%{query}%"))

        # 3. Cuenta el total de resultados (sin paginar) para saber cuántas páginas habrá.
        # Se usa una subquery para contar sobre los filtros ya aplicados.
        total = self.db.scalar(select(func.count()).select_from(
            results.subquery())) or 0

        if total == 0:
            return 0, []

        # 4. Calcula la página actual asegurando que no sea menor a 1 ni mayor al total de páginas.
        current_page = min(page, max(1, ceil(total/per_page)))

        # 5. Define la columna de ordenamiento dinámicamente.
        order_col = PostORM.id if order_by == "id" else func.lower(
            PostORM.title)

        # 6. Aplica el orden (ASC o DESC)
        results = results.order_by(
            order_col.asc() if direction == "asc" else order_col.desc())
        # results = sorted(
        #     results, key=lambda post: post[order_by], reverse=(direction == "desc"))

        # 7. Aplica Paginación (LIMIT y OFFSET)
        start = (current_page - 1) * per_page
        # execute(...).scalars().all(): Ejecuta la query y convierte las filas de BD a objetos ORM.
        items = self.db.execute(results.limit(
            per_page).offset(start)).scalars().all()

        return total, items

    def by_tags(self, tags: List[str]) -> List[PostORM]:
        normalized_tag_names = [tag.strip().lower()
                                for tag in tags if tag.strip()]

        if not normalized_tag_names:
            return []

        # Consulta avanzada con Joins
        post_list = (
            select(PostORM)
            .options(
                # Optimización: Carga tags y autor en la misma transacción para evitar el problema N+1
                selectinload(PostORM.tags),
                joinedload(PostORM.author),
            )
            # Filtra posts que tengan AL MENOS UNA etiqueta que coincida con la lista
            .where(PostORM.tags.any(func.lower(TagORM.name).in_(normalized_tag_names)))
            .order_by(PostORM.id.asc())
        )

        return self.db.execute(post_list).scalars().all()

    # Lógica "Get or Create" para Autores.
    # Si el autor ya existe por email, lo devuelve. Si no, crea una instancia nueva (sin guardar aún).
    def ensure_author(self, name: str, email: str) -> AuthorORM:

        author_obj = self.db.execute(
            select(AuthorORM).where(AuthorORM.email == email)
        ).scalar_one_or_none()

        if author_obj:
            return author_obj

        author_obj = AuthorORM(name=name,
                               email=email)
        self.db.add(author_obj)
        # flush(): Envía los datos a la BD para obtener un ID, pero NO confirma la transacción (commit).
        self.db.flush()

        return author_obj

    # Lógica "Get or Create" para Tags.
    def ensure_tag(self, name: str) -> TagORM:
        tag_obj = self.db.execute(
            select(TagORM).where(TagORM.name.ilike(name))
        ).scalar_one_or_none()

        if tag_obj:
            return tag_obj

        tag_obj = TagORM(name=name)
        self.db.add(tag_obj)
        self.db.flush()
        return tag_obj

    def create_post(self, title: str, content: str, author: Optional[dict], tags: List[dict]) -> PostORM:
        author_obj = None
        if author:
            author_obj = self.ensure_author(author['name'], author['email'])

        # Crea el objeto PostORM
        post = PostORM(title=title, content=content, author=author_obj)

        # Asocia los tags (creándolos si no existen)
        for tag in tags:
            tag_obj = self.ensure_tag(tag["name"])
            post.tags.append(tag_obj)

        # Agrega el post a la sesión. El commit final se hace en el router.
        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def update_post(self, post: PostORM, updates: dict) -> PostORM:
        for key, value in updates.items():
            setattr(post, key, value)

        return post

    def delete_post(self, post: PostORM) -> None:
        self.db.delete(post)