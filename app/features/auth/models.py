from pydantic import BaseModel, EmailStr
from typing import Literal

class UserInManual(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserInOAuth(BaseModel):
    email: EmailStr
    external_id: str
    first_name: str
    last_name: str
    login_type: Literal["google", "facebook"]

class TokenOut(BaseModel):
    token: str

class RefreshRequest(BaseModel):
    refresh_token: str
