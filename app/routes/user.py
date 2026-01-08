from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.schemas.auth import RegisterUser, ResponseUser
from app.repositories.user import UserRepository
from app.middleware.auth import is_admin
from app.database import get_db


router = APIRouter(tags=['Users'])



@router.post('/users', response_model=ResponseUser)
def register(request: RegisterUser, db: Session = Depends(get_db), _=Depends(is_admin)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    db_user = user_repo.register(request)

    return db_user

@router.get('/users', response_model=List[ResponseUser])
def get_users(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    _=Depends(is_admin)
):
    user_repo = UserRepository(db, PasswordHash.recommended())
    return user_repo.get_all_users(page, per_page)


@router.get('/users/{user_id}', response_model=ResponseUser)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    _=Depends(is_admin)
):
    user_repo = UserRepository(db, PasswordHash.recommended())
    return user_repo.get_user_by_id(user_id)


@router.put('/users/{user_id}', response_model=ResponseUser)
def update_user(
    user_id: int, 
    request: RegisterUser, 
    db: Session = Depends(get_db), 
    _=Depends(is_admin)
):
    user_repo = UserRepository(db, PasswordHash.recommended())
    return user_repo.update_user(user_id, request)


@router.delete('/users/{user_id}')
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    _=Depends(is_admin)
):
    user_repo = UserRepository(db, PasswordHash.recommended())
    user_repo.delete_user(user_id)

    return {'detail': 'Usuário deletado com sucesso.'}