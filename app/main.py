from fastapi import FastAPI, Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from .database import get_db
from .schemas.auth import LoginRequest, RegisterRequest
from .schemas.products import ProductCategorySchema
from .repositories.user import UserRepository
from .repositories.products import ProductCategoryRepository
from .middleware.auth import is_admin, is_auth


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
def register(request: RegisterRequest, db: Session = Depends(get_db), _=Depends(is_admin)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    db_user = user_repo.register(request)

    return {
        'username': db_user.username,
        'full_name': db_user.full_name,
        'email': db_user.email,
        'is_active': db_user.is_active,
    }


@app.post('/product/categories')
def create_product_category(category: ProductCategorySchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.create_product_category(category)


@app.get('/product/categories')
def get_product_categories(db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.get_all_categories()

@app.get('/product/categories/{category_id}')
def get_product_category(category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.get_category_with_id(category_id)

@app.put('/product/categories/{category_id}')
def update_product_category(category: ProductCategorySchema, category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    return product_category_repo.update_product_category(category_id, category)


@app.delete('/product/categories/{category_id}')
def delete_product_category(category_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_category_repo = ProductCategoryRepository(db)
    product_category_repo.delete_product_category(category_id)

    return {'detail': 'Categoria de produto deletada com sucesso.'}
