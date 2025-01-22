from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from ..services.user import get_user, register_user, authenticate_user
from ..scheemas.user import UserCreate, UserDetail, UserAuth
from ..dependencies.auth import create_access_token, get_current_user_name

from ..database import get_db_session


router = APIRouter()

@router.post("/login/")
def read_items(user: UserAuth):
    user_is_valid = authenticate_user(user) 
    if user_is_valid:
        token = create_access_token({"name": user.name})
        return {"token": token}
    else:
        raise HTTPException(status_code=404)

@router.post("/register/")
def new_user(user: UserCreate,  db = Depends(get_db_session)):
    register_user(db, user=user,)
    return 200


@router.get("/users/{user_id}")
def retriewe_user(user_id: int,  db = Depends(get_db_session)) -> UserDetail:
    user = get_user(user_id=user_id, db=db)
    return user