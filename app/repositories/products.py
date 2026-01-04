
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.products import ProductsCategories
from app.schemas.products import ProductCategorySchema

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