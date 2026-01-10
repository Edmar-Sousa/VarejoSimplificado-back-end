from pydantic import BaseModel, EmailStr, SecretStr, Field, validator
from typing import Optional


class RegisterUser(BaseModel):
    username: str = Field(..., example="Nome de Usuario")
    full_name: str = Field(..., example="Nome Completo")
    email: EmailStr = Field(..., example="Email válido")
    password: str = Field(..., example="Senha segura")

    business_id: Optional[int]

    @validator('password', pre=True)
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres.')

        return value


class ResponseUser(BaseModel):
    username: str = Field(..., example="Nome de Usuario")
    full_name: str = Field(..., example="Nome Completo")
    email: EmailStr = Field(..., example="Email válido")
    is_active: bool = Field(..., example=True)
    business_id: Optional[int]