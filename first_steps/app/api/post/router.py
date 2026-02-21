
from math import ceil
from fastapi import APIRouter, Query, HTTPException,Path,status,Depends
from typing import Optional,List,Union,Literal
from sqlalchemy.orm import Session
from app.core.db import get_db
from .schemas import (PostPublic, PostCreate, 
                      PostUpdate, PaginatedPost, PostSummary)
from .repository import PostRepository

router = APIRouter(prefix = "\posts", tags=["Posts"])

@router.get("", response_model=PaginatedPost)
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
    repository = PostRepository(db)
    query = query or text 
    total, items = repository.search(query, order_by, page, per_page, direction)

    total_pages = ceil(total/per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(page, total_pages)

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



