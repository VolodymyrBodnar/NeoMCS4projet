from pydantic import BaseModel, EmailStr

    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserDetail(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserAuth(BaseModel):
    name: str
    password: str 




