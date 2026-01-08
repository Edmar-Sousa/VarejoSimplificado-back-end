from pydantic import BaseModel, EmailStr, SecretStr, Field, validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="Email válido")
    password: str = Field(..., example="Senha segura")

    @validator('password', pre=True)
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres.')

        return value


class LoginResponse(BaseModel):
    access_token: str = Field(..., example="Token jwt")
    token_type: str = Field(..., example="Bearer")


class RegisterUser(BaseModel):
    username: str = Field(..., example="Nome de Usuario")
    full_name: str = Field(..., example="Nome Completo")
    email: EmailStr = Field(..., example="Email válido")
    password: str = Field(..., example="Senha segura")


class RegisterResponse(BaseModel):
    username: str = Field(..., example="Nome de Usuario")
    full_name: str = Field(..., example="Nome Completo")
    email: EmailStr = Field(..., example="Email válido")
    is_active: bool = Field(..., example=True)
