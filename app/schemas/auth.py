from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    username: str
    full_name: str
    email: str
    is_active: bool
