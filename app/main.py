from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from .database import get_db
from .repositories.products import ProductCategoryRepository, ProductRepository
from .schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from .schemas.products import ProductCategorySchema, ProductSchema
from .repositories.user import UserRepository
from .middleware.auth import is_admin, is_auth


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/login')
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    user = user_repo.login(request)

    access_token = user_repo.create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type='Bearer'
    )

@app.post('/register')
def register(request: RegisterRequest, db: Session = Depends(get_db), _=Depends(is_admin)):
    user_repo = UserRepository(db, PasswordHash.recommended())
    db_user = user_repo.register(request)

    return RegisterResponse(
        username=db_user.username,
        full_name=db_user.full_name,
        email=db_user.email,
        is_active=db_user.is_active,
    )


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


@app.get('/products')
def get_products(
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1), 
    token=Depends(is_auth)
):
    product_repo = ProductRepository(db)
    return product_repo.get_all_products(page, per_page)


@app.get('/products/{product_id}')
def get_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.get_product_with_id(product_id)


@app.post('/products')
def create_product(product: ProductSchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.create_product(product)


@app.put('/products/{product_id}')
def update_product(product_id: int, product: ProductSchema, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    return product_repo.update_product(product_id, product)


@app.delete('/products/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db), token=Depends(is_auth)):
    product_repo = ProductRepository(db)
    product_repo.delete_product(product_id)

    return {'detail': 'Produto deletado com sucesso.'}