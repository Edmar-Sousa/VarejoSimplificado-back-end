from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import is_auth
from app.repositories.products import ProductCategoryRepository
from app.schemas.products import ProductCategorySchema


router = APIRouter(
    prefix='/products', 
    tags=['Product Categories']
)

@router.post('/categories')
def create_product_category(category: ProductCategorySchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.create_product_category(category)


@router.get('/categories')
def get_product_categories(db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.get_all_categories()


@router.get('/categories/{category_id}')
def get_product_category(category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.get_category_with_id(category_id)


@router.put('/categories/{category_id}')
def update_product_category(category: ProductCategorySchema, category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.update_product_category(category_id, category)


@router.delete('/categories/{category_id}')
def delete_product_category(category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    product_category_repo.delete_product_category(category_id)

    return {'detail': 'Categoria de produto deletada com sucesso.'}
