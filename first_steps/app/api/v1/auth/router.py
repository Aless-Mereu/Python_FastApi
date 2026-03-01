from fastapi import APIRouter,Depends, HTTPException, status
from .schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token,get_current_user
from datetime import timedelta
from .schemas import UserPublic

# Base de datos simulada de usuarios (en memoria).
FAKE_USERS = {
    "alessandro@gmail.com": {"email": "alessandro@gmail.com", "username": "alessandro", "password": "password123"},
    "alumno@example.com": {"email": "alumno@example.com", "username": "alumno", "password": "password123"},

}

router = APIRouter(prefix="/auth", tags=["auth"])


# Endpoint de Login.
# OAuth2PasswordRequestForm: Dependencia de FastAPI que espera los datos
# como 'form-data' (username, password) en lugar de JSON.
@router.post("/login",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Busca el usuario en la "BD" usando el username enviado en el formulario.
    user=FAKE_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token(
        data={"sub": user["email"], "username": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    
    return {"access_token": token, "token_type": "bearer"}

# Endpoint protegido para obtener información del usuario actual.
# Usa la dependencia get_current_user para validar el token antes de ejecutar la lógica.
@router.get("/me",response_model=UserPublic)
async def read_me(current=Depends(get_current_user)):
    return {"email": current["email"], "username": current["username"]}
