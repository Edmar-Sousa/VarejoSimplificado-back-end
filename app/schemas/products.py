from pydantic import BaseModel


class ProductCategorySchema(BaseModel):
    name: str
    description: str
