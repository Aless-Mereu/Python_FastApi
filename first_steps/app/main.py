from fastapi import FastAPI, Query, HTTPException,Path,status,Depends
from pydantic import BaseModel, Field, field_validator,EmailStr,ConfigDict
from typing import Optional,List,Union,Literal
from math import ceil
from sqlalchemy import select,func
from sqlalchemy.orm import Session,selectinload,joinedload
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from dotenv import load_dotenv



#-----------CONFIGURACIÓN PARA BASE DE DATOS-----------------------------
load_dotenv()











Base.metadata.create_all(bind=engine) # dev


#----------------------------------------------------------------------------------------------------




app = FastAPI(title= "Mini blog")

#---------------------------------------------------CLASES---------------------------------------------------------------------------




#------------------------------------------------Servicios / Helpers-------------------------------------------------------------------------

def get_or_create_author(db: Session, author_in: Optional[Author]) -> Optional[AuthorORM]:
    if not author_in:
        return None

    author_obj = db.execute(
        select(AuthorORM).where(AuthorORM.email == author_in.email)
    ).scalar_one_or_none()

    if not author_obj:
        author_obj = AuthorORM(name=author_in.name, email=author_in.email)
        db.add(author_obj)
        db.flush()  # Genera el ID sin confirmar la transacción
    return author_obj

def get_or_create_tags(db: Session, tags_in: List[Tag]) -> List[TagsORM]:
    tag_names = {tag.name for tag in tags_in} # Set para eliminar duplicados de entrada
    existing_tags = db.execute(select(TagsORM).where(TagsORM.name.in_(tag_names))).scalars().all()
    existing_tag_names = {tag.name for tag in existing_tags}

    new_tags = [TagsORM(name=name) for name in tag_names if name not in existing_tag_names]
    if new_tags:
        db.add_all(new_tags)
        db.flush() # Para obtener IDs de los nuevos tags
    
    return list(existing_tags) + new_tags

#------------------------------------------------EndPoints-----------------------------------------------------------------------------------


@app.get("/")
def home():
    return {"message": "Bienvenidos a Mini Blog por Alessandro Garcia"}

@app.get("/posts",response_model=PaginatedPost,response_description="Lista de posts",status_code=200)
def list_posts(
    text: Optional[str] = Query(
    default=None,
    deprecated=True, 
    description = "Parámetro obsoleto, usa 'query o search' en su lugar.",
    
    ),
    
    query: Optional[str] = Query(
    default=None, 
    description = "Texto para buscar por título",
    alias="search",
    min_length=3,
    max_length=50,
    pattern=r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+$" #regex101.com
    ),

    per_page: int =Query(
        10, ge=1, le=50,
        description="Número de resultados de 1 a 50"
    ),
    page: int =Query(
        1, ge=1,
        description="Número de página (>=1)"
    ),
    order_by: Literal["id","title"] =Query(
        "id",description="campo de orden"
    ),
    direction: Literal["asc", "desc"] = Query(
        "asc", description="dirección de orden"
    ),
    db: Session = Depends(get_db)
):
    
    # results = select(PostORM)

    # query = query or text 
    
    # if query: 
    #     results = results.where(PostORM.title.ilike(f"{query}%"))

    # total = db.scalar(select(func.count())
    #                   .select_from(results.subquery())) or 0
    
    # total_pages = ceil(total/per_page) if total > 0 else 0

    # if total_pages == 0:
    #     current_page = 1
    # else:
    #     current_page = min(page, total_pages)
    

    # if order_by == "id":
    #     order_col = PostORM.id
    # else:
    #     order_col = PostORM.title
    
    # results = results.order_by(order_col.asc() if direction == "asc" else order_col.desc())

    

    # if total_pages == 0:
    #     items = []
    # else:
    #     start = (current_page-1)*per_page
    #     items = db.execute(results.offset(start).limit(per_page)).scalars().all()

    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages > 0 else False

    return PaginatedPost(
        page=current_page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        order_by=order_by,
        direction=direction,
        search=query,
        items=items
        
    )



#Path parameters + query parameter
@app.get("/posts/{post_id}",response_model=Union[PostPublic,PostSummary],response_description="Post encontrado")#evaise HTTPException(status_code=404, detail="Post no encontrado")alúa el primero y si no concuerda, evalúa al segundo parámetro
def get_post(post_id: int = Path(
        ...,
        ge=1,
        title = "ID de post",
        description="Identificador entero de post: debe ser mayor que 0",
        example=1
    ), include_content: bool = Query(default=True, description="query para ocultar content"),db : Session = Depends(get_db)):

        post = db.get(PostORM, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post no encontrado")    
         
        if include_content:
            return PostPublic.model_validate(post, from_attributes=True)
        
        return PostSummary.model_validate(post, from_attributes=True)


@app.get("/posts_by_tags", response_model =List[PostPublic])
def filter_by_tags(
    tags: List[str]=Query(
        description="una o más etiquetas. Ejemplo: ?tags=python&tags0fastapi "
    ),
    db: Session = Depends(get_db)

):
    # normalized_tag_names = [tag.strip().lower() for tag in tags if tag.strip()]
    # if not normalized_tag_names:
    #     return []
    
    # post_list= (
    #     select(PostORM)
    #     .options(
    #         selectinload(PostORM.tags),#evita el n+1 al serializar, crea una query para los post y después para las demás etiquetas
    #         joinedload(PostORM.author)
    #     ).where(PostORM.tags.any(func.lower(TagsORM.name).in_(normalized_tag_names)))
    #     .order_by(PostORM.created_at.asc()
    #     )
    # )
    # post =db.execute(post_list).scalars().all()
    return post
    


@app.post("/posts",response_model=PostPublic,response_description="Post creado (ok)",status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        author_obj = get_or_create_author(db, post.author)
        new_post = PostORM(title=post.title, content = post.content, author = author_obj)

        if post.tags:
            new_post.tags = get_or_create_tags(db, post.tags)

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except IntegrityError as e:
        db.rollback()
        print(f"Error de integridad: {e}")
        raise HTTPException(status_code=409, detail="El título del post ya existe o hay un conflicto de datos.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el post: {e}")
    except Exception as e:
        db.rollback()
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.put("/posts/{post_id}",response_model=PostPublic,response_description="Post actualizado",response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):

    post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")    
    
    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)
    return post
        


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int, db: Session = Depends(get_db)):
    post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")    
    
    db.delete(post)
    db.commit()
    return 
