from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRoles(Enum):
    admin = "ADMIN"
    employee = "EMPLOYEE"
    manager = "MANAGER"


class UserBase(BaseModel):
    name: str
    email: EmailStr | None


class UserCreate(UserBase):
    password: str


class UserDetail(UserBase):
    id: int
    role: str | None
    password: str


class AuthenticatedUser(BaseModel):
    role: str | None
    name: str


class UserAuth(BaseModel):
    name: str
    password: str
