from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.repositories.user import UserRepository
from app.middleware.auth import is_admin
from app.database import get_db


router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    user = user_repo.login(request)

    access_token = user_repo.create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type='Bearer'
    )


@router.post('/register')
def register(request: RegisterRequest, db: Session = Depends(get_db), _=Depends(is_admin)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    db_user = user_repo.register(request)

    return RegisterResponse(
        username=db_user.username,
        full_name=db_user.full_name,
        email=db_user.email,
        is_active=db_user.is_active,
    )
