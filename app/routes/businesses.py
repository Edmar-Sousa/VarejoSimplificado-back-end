from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy.orm import Session

from app.middleware.auth import is_admin
from app.database import get_db
from app.schemas.business import BusinessSchema, BusinessResponse

from app.repositories.business import BusinessRepository


router = APIRouter(tags=['Businesses'])


@router.post('/businesses', response_model=BusinessResponse)
def create_businesses(request: BusinessSchema, db: Session = Depends(get_db), admin: bool = Depends(is_admin)):
    business_repo = BusinessRepository(db)
    return business_repo.create_business(request)


@router.get('/businesses', response_model=List[BusinessResponse])
def get_all_businesses(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1), 
    token=Depends(is_admin)
):
    business_repo = BusinessRepository(db)
    return business_repo.get_all_businesses(page, per_page)


@router.get('/businesses/{business_id}', response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db), token=Depends(is_admin)):
    business_repo = BusinessRepository(db)
    return business_repo.get_business(business_id)


@router.put('/businesses/{business_id}', response_model=BusinessResponse)
def update_business(business_id: int, request: BusinessSchema, db: Session = Depends(get_db), token=Depends(is_admin)):
    business_repo = BusinessRepository(db)
    return business_repo.update_business(business_id, request)


@router.delete('/businesses/{business_id}')
def delete_business(business_id: int, db: Session = Depends(get_db), token=Depends(is_admin)):
    business_repo = BusinessRepository(db)
    business_repo.delete_business(business_id)

    return {'detail': 'Business deleted successfully.'}