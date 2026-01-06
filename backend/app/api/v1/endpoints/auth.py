"""
Endpoints de autenticación: login, register, logout
"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.params import Depends
from backend.app.core.database import get_db
from backend.app.core.security import (
    hash_password, verify_password, create_access_token, create_refresh_token
)
from backend.app.core.dependencies import get_current_user
from backend.app.core.ratelimit import limiter
from backend.app.models.user import User
from backend.app.schemas.auth import (
    LoginRequest, RegisterRequest, Token, PasswordResetRequest
)
from backend.app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario
    
    - **email**: Email único del usuario
    - **username**: Username único (3-100 caracteres)
    - **full_name**: Nombre completo (3+ caracteres)
    - **password**: Contraseña (8+ caracteres)
    - **phone**: Teléfono (opcional)
    """
    
    # Verificar si el email ya existe
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    
    # Verificar si el username ya existe
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ya existe"
        )
    
    # Crear nuevo usuario
    new_user = User(
        email=request.email,
        username=request.username,
        full_name=request.full_name,
        hashed_password=hash_password(request.password),
        phone=request.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # limit login attempts to mitigate brute-force
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login: obtener token de acceso
    
    - **email**: Email del usuario
    - **password**: Contraseña
    
    Retorna:
    - **access_token**: JWT token para usar en endpoints protegidos
    - **refresh_token**: Token para obtener nuevo access_token
    """
    
    # Buscar usuario por email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear tokens
    access_token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role.value
    })
    
    refresh_token = create_refresh_token(data={
        "sub": str(user.id)
    })
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    """
    Logout: invalida el token actual (cliente)
    
    En la práctica, el logout se maneja desde el frontend
    eliminando el token del localStorage.
    Este endpoint es opcional para implementar blacklist en backend.
    """
    return {"message": "Logout exitoso"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información del usuario actual (autenticado)
    
    Requiere: Header Authorization: Bearer {token}
    """
    user_obj = db.query(User).filter(User.id == int(user["user_id"])).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user_obj


@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    """
    Refrescar access token usando refresh token
    
    - **refresh_token**: Token de refresco obtenido en login
    
    Retorna nuevo access_token y refresh_token
    """
    from backend.app.core.security import verify_refresh_token
    
    try:
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")
        
        new_access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )
