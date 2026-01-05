from pydantic import BaseModel


class ProductCategorySchema(BaseModel):
    name: str
    description: str


class ProductSchema(BaseModel):
    description: str
    bar_code: str
    quantity: int
    category_id: int
