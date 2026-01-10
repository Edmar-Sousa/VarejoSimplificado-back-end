from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import is_auth
from app.repositories.products import ProductRepository
from app.schemas.products import ProductSchema


router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.get('/')
def get_products(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1), 
    token=Depends(is_auth)
):
    product_repo = ProductRepository(db)
    return product_repo.get_all_products(page, per_page)


@router.get('/{product_id}')
def get_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.get_product_with_id(product_id)


@router.post('/')
def create_product(product: ProductSchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.create_product(product)


@router.put('/{product_id}')
def update_product(
    product_id: int, 
    product: ProductSchema, 
    db: Session = Depends(get_db), 
    token=Depends(is_auth)
):
    product_repo = ProductRepository(db)
    return product_repo.update_product(product_id, product)


@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    product_repo.delete_product(product_id)

    return {'detail': 'Produto deletado com sucesso.'}