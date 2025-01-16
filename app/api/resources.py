from fastapi import APIRouter, Depends

from ..scheemas.resources import ResourceCreate, ResourceDetail
from ..services.resources import create_item, get_item, get_all, update_item
from ..repositories.resources import  delete_one
from ..database import get_db_session


router = APIRouter()

@router.post("/resources/")
def create_resource(item: ResourceCreate, db = Depends(get_db_session))->ResourceCreate:
    result = create_item(item, db)
    return result


@router.get("/resources/{id}")
def get_one(id: int)->ResourceDetail:
    return get_item(id)


@router.get("/resources/")
def list_view()->list[ResourceDetail]:
    return get_all()


@router.put("/resources/{id}")
def update(id: int, data: ResourceCreate)->ResourceCreate:
    return update_item(id, data)


@router.delete("/resources/{id}")
def delete(id: int):
    delete_one(id)
