from ..scheemas.user import UserCreate, UserDetail

def get_user_from_db(id):
    return UserDetail(id=id,name="ASDsad",email="jhondou@gmail.com")


def create_user(user: UserCreate):
    print(user)

def get_user(user_id: int) -> UserDetail:
    return  get_user_from_db(user_id)


def update_user(user_id:int, user_data: UserDetail):
    ...

def delete_user(user_id: int):
    ...