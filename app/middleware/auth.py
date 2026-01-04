import os

from jose import jwt
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Token de autenticação inválido.')


def is_admin(user_payload = Depends(get_current_user)):

    if user_payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Acesso negado. Permissões insuficientes.')

    return user_payload
