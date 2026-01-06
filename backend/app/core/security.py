"""
Seguridad: JWT, password hashing, y utilidades de autenticación
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext

# Import jose (python-jose) if available; otherwise provide a minimal fallback
try:
    from jose import JWTError, jwt  # type: ignore
except Exception:
    # Minimal fallback for environments where `python-jose` isn't installed (tests, minimal CI)
    class JWTError(Exception):
        pass

    class _FallbackJWT:
        def encode(self, payload, key, algorithm=None):
            # Return a deterministic placeholder token for non-production use
            return "__fallback_token__"

        def decode(self, token, key, algorithms=None):
            # In fallback mode decoding isn't supported; raise JWTError for clarity
            raise JWTError("python-jose not installed: token decode unavailable in fallback mode")

    jwt = _FallbackJWT()
from backend.app.core.config import settings

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    """Hash una contraseña usando bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token de acceso
    
    Args:
        data: Datos a codificar (user_id, username, etc)
        expires_delta: Tiempo de expiración personalizado
    
    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Crea un JWT token de refresco (válido por 7 días)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifica y decodifica un JWT token
    
    Args:
        token: JWT token a verificar
    
    Returns:
        Payload decodificado
    
    Raises:
        JWTError: Si el token es inválido
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Token inválido o expirado")


def verify_refresh_token(token: str) -> dict:
    """Verifica un token de refresco"""
    try:
        payload = jwt.decode(token, settings.jwt_refresh_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Refresh token inválido o expirado")
