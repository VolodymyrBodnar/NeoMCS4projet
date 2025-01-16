from pydantic import BaseModel, EmailStr

    
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserDetail(BaseModel):
    id: int
    name: str
    email: EmailStr




