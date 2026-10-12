from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


Role = Literal["admin", "sales_manager", "sales_rep"]


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminCreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    role: Role


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    is_active: bool

    model_config = ConfigDict(from_attributes=True)