from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from .database import get_db
from .repositories.products import ProductRepository
from .schemas.products import ProductSchema
from .middleware.auth import is_auth

from .routes.auth import router as auth_router
from .routes.products.categories import router as product_categories_router
from .routes.products import router as products_router

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

app.include_router(auth_router)
app.include_router(product_categories_router)
app.include_router(products_router)
