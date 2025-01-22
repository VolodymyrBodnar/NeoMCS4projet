from typing import Any
from ..scheemas.user import UserCreate, UserDetail, UserAuth
from ..repositories.user import create_new, get_item_from_db, get_user_from_db_by_name

import hashlib


def salted_hash(data: str):
    password = data +  "secret_part"
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(db, user: UserCreate):
    user.password = salted_hash(user.password)
    return create_new(user, db)


def get_user(user_id: int, db: Any) -> UserDetail:
    return  get_item_from_db(user_id, db)

def authenticate_user(user: UserAuth):
    name = user.name
    password = user.password
    user_from_db = get_user_from_db_by_name(name)
    hashed_pass = salted_hash(password)
    print(hashed_pass)
    print(user_from_db.password)
    return hashed_pass == user_from_db.password
        




def update_user(user_id:int, user_data: UserDetail):
    ...

def delete_user(user_id: int):
    ...