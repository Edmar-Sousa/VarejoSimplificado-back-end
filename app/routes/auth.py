from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.schemas.auth import LoginRequest, LoginResponse, RegisterAdmin, ResponseAdmin
from app.repositories.user import UserRepository
from app.database import get_db


router = APIRouter(tags=['Auth'])

@router.post('/login', response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    user = user_repo.login(request)

    access_token = user_repo.create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "business_id": user.business_id,
        }
    )

    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }


@router.post('/register', response_model=ResponseAdmin)
def register(request: RegisterAdmin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    return user_repo.register_admin(request, 'admin')
