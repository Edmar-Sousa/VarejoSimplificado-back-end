from typing import List
from datetime import datetime
from sqlalchemy import String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .database import Base


class ProductsCategories(Base):
    __tablename__ = 'products_categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(index=True)


class Products(Base):
    __tablename__ = 'products'
   
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column()
    bar_code: Mapped[str] = mapped_column(unique=True, index=True)

    quantity: Mapped[int] = mapped_column()

    category_id: Mapped[int] = mapped_column(ForeignKey('products_categories.id'))
    category: Mapped['ProductsCategories'] = relationship('ProductsCategories', back_populates='products')
