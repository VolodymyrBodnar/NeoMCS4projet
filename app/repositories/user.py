from ..scheemas.user import UserCreate, UserAuth, UserDetail
from ..models.users import User
from ..database import SessionLocal


def create_new(data: UserCreate, db) -> UserCreate:
    db = SessionLocal()
    new_user = User()
    new_user.name = data.name
    new_user.email = data.email
    new_user.password = data.password
    # try:
    with db.begin():
        db.add(new_user)
        db.commit()
    # except Exception:
    #     print("ERROR")
    # else:
    return data


def get_item_from_db(id: int, db: SessionLocal) -> UserDetail:
    db = SessionLocal()

    with db.begin():
        item = db.query(User).filter(User.id == id).first()
        if item is not None:
            return UserDetail(id=item.id, name=item.name, email=item.email)
    # except Exception:
    #     print("ERROR")


def get_user_from_db_by_name(name):
    db = SessionLocal()
    with db.begin():
        item = db.query(User).filter(User.name == name).first()
        if item is not None:
            return UserDetail(
                id=item.id,
                email=None,
                name=item.name,
                role=item.role,
                password=item.password,
            )


def get_all_from_db() -> list[User]:
    db = SessionLocal()
    try:
        with db.begin():
            result = db.query(User).all()
            db.expunge_all()
            return result
    except Exception:
        print("ERROR")


def update_user_in_db(name, data):
    db = SessionLocal()
    # try:
    with db.begin():
        item = db.query(User).filter(User.name == name).first()
        item.role = data.role
        db.commit()
    # except Exception:
    #     print("ERROR")
    # else:
    return data


# def delete_one(id):
#     db = SessionLocal()
#     try:
#         with db.begin():
#             item = db.query(Resource).filter(Resource.id == id).first()
#             db.delete(item)
#             db.commit()
#     except Exception:
#         print("ERROR")
# s
