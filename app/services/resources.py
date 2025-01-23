from uuid import uuid4

from fastapi.exceptions import HTTPException

from ..scheemas.resources import ResourceCreate, ResourceDetail
from ..repositories.resources import (
    create_new,
    get_item_from_db,
    get_all_from_db,
    update_item_in_db,
)


def create_item(item: ResourceCreate, db) -> ResourceCreate:
    item.description = f"{item.description}. UUID: {str(uuid4())}"
    return create_new(item, db)


def get_item(item_id: int) -> ResourceDetail:
    result = get_item_from_db(item_id)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404)


def get_all() -> list[ResourceDetail]:
    items_from_db = get_all_from_db()
    return [
        ResourceDetail(name=item.name, description=item.description, id=item.id)
        for item in items_from_db
    ]


def update_item(id: int, data: ResourceCreate):
    result = update_item_in_db(id, data)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404)
