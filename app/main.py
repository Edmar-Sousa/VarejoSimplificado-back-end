from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .schemas.auth import LoginRequest
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


@app.post('/login')
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(Users).where(Users.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail='Usuário com o email fornecido não foi encontrado.')
    
    password_hasher = PasswordHash.recommended()

    if not password_hasher.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Senha esta incorreta.')


    return {
        'user': request.email,
        'password': request.password
    }

