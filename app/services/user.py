from typing import Any
from ..scheemas.user import UserCreate, UserDetail, UserAuth
from ..repositories.user import (
    create_new,
    get_item_from_db,
    get_user_from_db_by_name,
    update_user_in_db,
)

import hashlib


def salted_hash(data: str):
    password = data + "secret_part"
    # we use hashlib.sha256 insteadof built in hash cause builtin yileds differet results
    # TODO use different algo
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(db, user: UserCreate):
    user.password = salted_hash(user.password)
    return create_new(user, db)


def get_user(user_id: int, db: Any) -> UserDetail:
    return get_item_from_db(user_id, db)


def authenticate_user(user: UserAuth):
    """
    Function to authenticate user with password, check if password is correct.

    Args:
        user(UserAuth): user data with pass
    Returns:
        user_from_db: data of authenticated user    
    """
    name = user.name
    password = user.password
    user_from_db = get_user_from_db_by_name(name)
    hashed_pass = salted_hash(password)
    if hashed_pass == user_from_db.password:
        return user_from_db


def update_user_role(user_data: UserDetail):
    update_user_in_db(user_data.name, user_data)


def delete_user(user_id: int): ...
