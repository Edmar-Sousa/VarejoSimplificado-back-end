from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessSchema

class BusinessRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_business(self, business_data: BusinessSchema):
        business = Business(
            full_name=business_data.full_name,
            email=business_data.email,
            phone=business_data.phone,
            cnpj=business_data.cnpj,
            is_active=business_data.is_active
        )
        
        self.db_session.add(business)
        self.db_session.commit()
        self.db_session.refresh(business)

        return business


    def get_all_businesses(self, page: int, per_page: int):
        businesses = self.db_session.query(Business).offset((page - 1) * per_page).limit(per_page).all()
        return businesses


    def get_business(self, business_id: int):
        business = self.db_session.query(Business).where(Business.id == business_id).first()

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Business not found.'
            )
        
        return business


    def update_business(self, business_id: int, business_data: BusinessSchema):
        business = self.db_session.query(Business).where(Business.id == business_id).first()

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Business not found.'
            )
        
        business.full_name = business_data.full_name
        business.email = business_data.email
        business.phone = business_data.phone
        business.cnpj = business_data.cnpj
        business.is_active = business_data.is_active

        self.db_session.commit()
        self.db_session.refresh(business)

        return business


    def delete_business(self, business_id: int):
        business = self.db_session.query(Business).where(Business.id == business_id).first()

        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Business not found.'
            )
        
        self.db_session.delete(business)
        self.db_session.commit()
