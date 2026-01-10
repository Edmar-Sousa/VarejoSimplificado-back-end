
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.products import Products, ProductsCategories
from app.schemas.products import ProductCategorySchema, ProductSchema

class ProductCategoryRepository:
    

    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_all_categories(self):
        categories = self.db_session.query(ProductsCategories).all()
        return categories
    

    def get_category_with_id(self, category_id: int):
        category = self.db_session.query(ProductsCategories).where(ProductsCategories.id == category_id).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Categoria de produto não encontrada.'
            )

        return category
    

    def delete_product_category(self, category_id: int):
        category = self.db_session.query(ProductsCategories).where(ProductsCategories.id == category_id).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Categoria de produto não encontrada.'
            )

        self.db_session.delete(category)
        self.db_session.commit()


    def update_product_category(self, category_id: int, category_data: ProductCategorySchema):
        category = self.db_session.query(ProductsCategories).where(ProductsCategories.id == category_id).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Categoria de produto não encontrada.'
            )

        category.name = category_data.name
        category.description = category_data.description

        self.db_session.commit()
        self.db_session.refresh(category)

        return category
    

    def create_product_category(self, category_data: ProductCategorySchema):
        new_category = ProductsCategories(
            name=category_data.name,
            description=category_data.description
        )

        self.db_session.add(new_category)
        self.db_session.commit()
        self.db_session.refresh(new_category)

        return new_category
    

class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_all_products(self, page: int, per_page: int, business_id: int | None):
        products = self.db_session.query(Products)

        if business_id is not None:
            products = products.where(Products.business_id == business_id)

        return products.offset((page - 1) * per_page).limit(per_page).all()
    

    def get_product_with_id(self, product_id: int, business_id: int | None):
        product = self.db_session.query(Products).where(Products.id == product_id)

        if business_id is not None:
            product = product.where(Products.business_id == business_id)
        
        product = product.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Produto não encontrado.'
            )

        return product
    

    def create_product(self, product_data: ProductSchema, business_id: int | None):

        business_id = business_id if business_id is not None else product_data.business_id

        if business_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='O ID do negócio deve ser fornecido.'
            )

        new_product = Products(
            description=product_data.description,
            bar_code=product_data.bar_code,
            quantity=product_data.quantity,
            price=product_data.price,
            category_id=product_data.category_id,
            business_id=business_id
        )

        self.db_session.add(new_product)
        self.db_session.commit()
        self.db_session.refresh(new_product)

        return new_product
    

    def delete_product(self, product_id: int, business_id: int | None):
        product = self.db_session.query(Products).where(Products.id == product_id)

        if business_id is not None:
            product = product.where(Products.business_id == business_id)

        product = product.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Produto não encontrado.'
            )

        self.db_session.delete(product)
        self.db_session.commit()

    
    def update_product(self, product_id: int, product_data: ProductSchema, business_id: int | None):
        product = self.db_session.query(Products).where(Products.id == product_id)

        if business_id is not None:
            product = product.where(Products.business_id == business_id)

        product = product.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Produto não encontrado.'
            )

        product.description = product_data.description
        product.bar_code = product_data.bar_code
        product.quantity = product_data.quantity
        product.category_id = product_data.category_id
        product.price = product_data.price

        if business_id is not None:
            product.business_id = business_id

        self.db_session.commit()
        self.db_session.refresh(product)

        return product