import os

from jose import jwt
from fastapi import HTTPException
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session


from app.schemas.auth import LoginRequest, RegisterRequest
from app.models.user import Users


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



class UserRepository:
    
    def __init__(self, db_session: Session, password_hasher: PasswordHash):
        self.db_session = db_session
        self.password_hasher = password_hasher


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        now = datetime.now(timezone.utc)
        expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        to_encode.update({"iat": now, "nbf": now, "exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt


    def login(self, user_credentials: LoginRequest):
        user = self.db_session.query(Users).where(Users.email == user_credentials.email).first()

        if not user:
            raise HTTPException(status_code=404, detail='Usuário com o email fornecido não foi encontrado.')

        if not self.password_hasher.verify(user_credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Senha esta incorreta.')
        
        return user


    def register(self, user_data: RegisterRequest, role: str = 'user'):

        db_user = Users(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=self.password_hasher.hash(user_data.password),
            is_active=True,
            role=role
        )

        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)

        return db_user