from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.middleware.auth import is_auth
from app.repositories.products import ProductRepository
from app.schemas.products import ProductSchema, ProductResponseSchema


router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.get('/', response_model=List[ProductResponseSchema])
def get_products(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1), 
    token=Depends(is_auth)
):
    product_repo = ProductRepository(db)
    return product_repo.get_all_products(page, per_page, token['business_id'])


@router.get('/{product_id}', response_model=ProductResponseSchema)
def get_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.get_product_with_id(product_id, token['business_id'])


@router.post('/', response_model=ProductResponseSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.create_product(product, token['business_id'])


@router.put('/{product_id}', response_model=ProductResponseSchema)
def update_product(
    product_id: int, 
    product: ProductSchema, 
    db: Session = Depends(get_db), 
    token=Depends(is_auth)
):
    product_repo = ProductRepository(db)
    return product_repo.update_product(product_id, product, token['business_id'])


@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    product_repo.delete_product(product_id)

    return {'detail': 'Produto deletado com sucesso.'}