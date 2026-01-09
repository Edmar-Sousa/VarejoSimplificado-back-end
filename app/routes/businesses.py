from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy.orm import Session

from app.middleware.auth import is_admin
from app.database import get_db


router = APIRouter(tags=['Businesses'])


@router.post('/businesses')
def create_businesses():
    pass

@router.get('/businesses')
def get_all_businesses():
    pass