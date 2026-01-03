import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import Base, SessionLocal, engine
from .schemas.auth import LoginRequest, RegisterRequest
from .models.user import Users


from pwdlib import PasswordHash

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"iat": now, "nbf": now, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


@app.post('/login')
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(Users).where(Users.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail='Usuário com o email fornecido não foi encontrado.')
    
    password_hasher = PasswordHash.recommended()

    if not password_hasher.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Senha esta incorreta.')


    return {
        'access_token': create_access_token(
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
    password_hasher = PasswordHash.recommended()

    db_user = Users(
        username=request.username,
        full_name=request.full_name,
        email=request.email,
        hashed_password=password_hasher.hash(request.password),
        is_active=True,
        role='admin'
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        'username': db_user.username,
        'full_name': db_user.full_name,
        'email': db_user.email,
        'is_active': db_user.is_active,
    }
