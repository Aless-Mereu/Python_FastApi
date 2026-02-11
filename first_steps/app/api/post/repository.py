from typing import Optional,List,Tuple
from sqlalchemy.orm import Session,selectinload,joinedload
from app.models.post import PostORM,AuthorORM,TagsORM
from sqlalchemy import select,func,text
from math import ceil



class PostRepository:
    def __init__(self,db:Session):
        self.db = db


    def get(self, post_id: int)-> Optional[PostORM]:
        post_find = select(PostORM).where(PostORM.id == post_id)
        post = self.db.execute(post_find).scalar_one_or_none()
        return post
    

    def search(
            self,
            query: Optional[str],
            order_by: str,
            page:int,
            per_page:int,
            direction:str
    ) -> Tuple[int , List[PostORM]]:
        
        results = select(PostORM)
        query = query or text 
    
        if query: 
           results = results.where(PostORM.title.ilike(f"{query}%"))

        total = self.db.scalar(select(func.count())
                      .select_from(results.subquery())) or 0
        if total == 0:
            return 0, []

        current_page = min(page, max(ceil(total/per_page)))

        order_col = PostORM.id if order_by == "id" else func.lower(PostORM.title)
    
        results = results.order_by(order_col.asc() if direction == "asc" else order_col.desc())

        start = (current_page-1)*per_page
        items = self.db.execute(results.offset(start)
                                .limit(per_page)).scalars().all()
        return total, items
    

    def by_tags(self,tag_names: List[str])-> List[PostORM]:
        normalized_tag_names = [tag.strip().lower() 
                                 for tag in tag_names if tag.strip()]

        if not normalized_tag_names:
            return []
         
        post_list= (
            select(PostORM)
            .options(
            selectinload(PostORM.tags),#evita el n+1 al serializar, crea una query para los post y después para las demás etiquetas
            joinedload(PostORM.author)
        ).where(PostORM.tags.any(func.lower(TagsORM.name).in_(normalized_tag_names)))
        .order_by(PostORM.created_at.asc()
        )
    )
        post =self.db.execute(post_list).scalars().all()
        return post


    def ensure_author(self,name: str, email: str) -> AuthorORM:
        author_obj = self.db.execute(
            select(AuthorORM).where(AuthorORM.email == email)
        ).scalar_one_or_none()

        if author_obj:
            return author_obj
        
        author_obj = AuthorORM(name=name, email=email)
        self.db.add(author_obj)
        self.db.flush()  # Genera el ID sin confirmar la transacción

        return author_obj


    def ensure_tag(self,name: str)-> TagsORM:
       tag_obj = self.db.execute(
            select(TagsORM).where(TagsORM.name.ilike(name)
        ).scalar_one_or_none())

       if tag_obj:
            return tag_obj
        
       tag_obj = TagsORM(name=name)
       self.db.add(tag_obj)
       self.db.flush()  # Genera el ID sin confirmar la transacción
       return tag_obj



    
        