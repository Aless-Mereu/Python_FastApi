from pydantic import BaseModel,ConfigDict
from typing import Optional



# Esquema para devolver el token de acceso al cliente tras el login.
class Token (BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
# Esquema para los datos internos del token (payload).
class TokenData(BaseModel):
    sub: str 
    username: str
    model_config = ConfigDict(from_attributes=True)
    
# Esquema para mostrar información pública del usuario (sin password).
class UserPublic (BaseModel):
    email: str
    username: str
    model_config = ConfigDict(from_attributes=True)