from fastapi import FastAPI, Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from .database import get_db
from .schemas.auth import LoginRequest, RegisterRequest
from .repositories.user import UserRepository


app = FastAPI()



@app.post('/login')
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    user = user_repo.login(request)

    return {
        'access_token': user_repo.create_access_token(
            data={
                "sub": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        ),
        'token_type': 'Bearer'
    }


@app.post('/register')
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    db_user = user_repo.register(request)

    return {
        'username': db_user.username,
        'full_name': db_user.full_name,
        'email': db_user.email,
        'is_active': db_user.is_active,
    }
