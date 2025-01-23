from ..scheemas.resources import ResourceCreate, ResourceDetail
from ..models.resources import Resource
from ..database import SessionLocal


def create_new(data: ResourceCreate, db) -> ResourceCreate:
    new_item = Resource()
    new_item.description = data.description
    new_item.name = data.name
    try:
        with db.begin():
            db.add(new_item)
            db.commit()
    except Exception:
        print("ERROR")
    else:
        return data


def get_item_from_db(id: int) -> ResourceDetail:
    db = SessionLocal()
    try:
        with db.begin():
            item = db.query(Resource).filter(Resource.id == id).first()
            if item is not None:
                return ResourceDetail(
                    id=item.id, name=item.name, description=item.description
                )
    except Exception:
        print("ERROR")


def get_all_from_db() -> list[Resource]:
    db = SessionLocal()
    try:
        with db.begin():
            result = db.query(Resource).all()
            db.expunge_all()
            return result
    except Exception:
        print("ERROR")


def update_item_in_db(id, data):
    db = SessionLocal()
    try:
        with db.begin():
            item = db.query(Resource).filter(Resource.id == id).first()
            item.name = data.name
            item.description = data.description
            db.commit()
    except Exception:
        print("ERROR")
    else:
        return data


def delete_one(id):
    db = SessionLocal()
    try:
        with db.begin():
            item = db.query(Resource).filter(Resource.id == id).first()
            db.delete(item)
            db.commit()
    except Exception:
        print("ERROR")
