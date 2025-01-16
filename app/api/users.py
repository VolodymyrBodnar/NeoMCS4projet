from fastapi import APIRouter

from ..services.user import get_user, create_user
from ..scheemas.user import UserCreate, UserDetail


router = APIRouter()

@router.post("/users")
def new_user(user: UserCreate):
    create_user(user=user)
    return 200


@router.get("/users/{user_id}")
def retriewe_user(user_id: int) -> UserDetail:
    return get_user(user_id)
