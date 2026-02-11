from pydantic import BaseModel, Field, field_validator,EmailStr,ConfigDict
from typing import Optional,List,Literal


class Tag (BaseModel):
    name: str = Field(..., min_length=2, max_length=30, description="Nombre de la etiqueta")

    model_config = ConfigDict(from_attributes=True)# acepta objetos del ORM


class Author(BaseModel):
    name:str
    email:EmailStr

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str
    content: str
    #content: Optional[str]="Contenido no disponible"
    tags: Optional[List[Tag]] = Field(default_factory=list) #crea una lista vacía pero asegura crear una lista por cada objeto
    author: Optional[Author] = None

    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Título de del Post (mínimo 3 caractéres y máximo 100)",
        examples=["Mi primer post con FastAPI"]

    )
    content: Optional[str] = Field(
        default="Contenido no disponible",
        min_length=10,
        description="Mínimo 10 caracteres",
        examples=["Este es un contenido válido porque tiene 10 caracteres  o más"]
    )

    tags: List[Tag] = Field(default_factory=list)
    author: Optional[Author] = None

    @field_validator("title") #evalua el campo title
    @classmethod #acceso a la clase completa
    def not_allowed_title(cls, value:str)-> str:
        palabras_prohibidas = ["porn", "xxx", "spam"]
        for palabra in palabras_prohibidas:
            if palabra in value.lower():
                raise ValueError("El título no puede contener la palabra: " + palabra)
        return value


class PostUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100) 
    content: Optional[str] = None #el campo se vuelve opcional


class PostPublic(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)#convierte a Json
   

class PostSummary(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True) #también vamos a validar objetos


class PaginatedPost (BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id","title"]
    direction: Literal["asc", "desc"]
    search: Optional[str]=None
    items: List[PostPublic]

