import os
from datetime import datetime, timedelta,timezone
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import Depends, HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError


# Configuración de seguridad.
# SECRET_KEY: Clave secreta para firmar los tokens. En producción debe ser larga, aleatoria y segura.
SECRET_KEY = os.getenv("SECRET_KEY","change_me_in_production")
ALGORITHM = "HS256" # Algoritmo de encriptación (HMAC con SHA-256)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# OAuth2PasswordBearer: Esquema de seguridad que le dice a FastAPI que el cliente
# debe enviar el token en el header "Authorization: Bearer <token>".
# tokenUrl: URL relativa donde el cliente puede obtener el token (login).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Excepción reutilizable para errores de autenticación (401 Unauthorized).
credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    
def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permiso para acceder a este recurso",
    )
 

# Función para generar el JWT (JSON Web Token).
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # Define la fecha de expiración.
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # Codifica el diccionario a un string JWT firmado.
    token = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


# Decodifica y valida la firma del token.
def decode_token(token: str)-> dict:
    playload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return playload


# Dependencia para obtener el usuario actual a partir del token.
# Se ejecuta en cada endpoint protegido para validar la sesión.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        playload = decode_token(token)
        sub: Optional[str] = playload.get("sub")
        username: Optional[str] = playload.get("username")
        if not sub or not username:
            raise credentials_exc
        return {"email": sub, "username": username}
    except ExpiredSignatureError:
        raise raise_expired_token()
    except jwt.InvalidTokenError:
        raise credentials_exc