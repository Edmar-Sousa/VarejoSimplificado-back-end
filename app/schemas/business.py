from pydantic import BaseModel, EmailStr, SecretStr, Field, validator
from typing import Optional


class BusinessSchema(BaseModel):
    full_name: str = Field(..., example="Full name")
    email: EmailStr = Field(..., example="email@example.com")
    cnpj: str = Field(..., example="00.000.000/0000-00")
    phone: str = Field(..., example="+5511999999999")
    is_active: bool = Field(..., example=True)


class BusinessResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    cnpj: str
    phone: str
    is_active: bool
