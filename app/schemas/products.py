from pydantic import BaseModel


class ProductCategorySchema(BaseModel):
    name: str
    description: str


class ProductSchema(BaseModel):
    description: str
    bar_code: str
    quantity: int
    price: int
    category_id: int

class ProductResponseSchema(BaseModel):
    id: int
    description: str
    bar_code: str
    quantity: int
    price: int
    category_id: int
    business_id: int