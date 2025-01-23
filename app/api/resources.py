from fastapi import APIRouter, Depends

from ..scheemas.resources import ResourceCreate, ResourceDetail
from ..services.resources import create_item, get_item, get_all, update_item
from ..repositories.resources import delete_one
from ..database import get_db_session
from app.dependencies.auth import AdminUser, Manager, Employee

router = APIRouter()


@router.post("/resources/")
def create_resource(
    item: ResourceCreate, user: Manager, db=Depends(get_db_session)
) -> ResourceCreate:
    result = create_item(item, db)
    return result


@router.get("/resources/{id}")
def get_one(id: int, user: Employee) -> ResourceDetail:
    return get_item(id)


@router.get("/resources/")
def list_view(user: Employee) -> list[ResourceDetail]:
    return get_all()


@router.put("/resources/{id}")
def update(id: int, data: ResourceCreate, user: Manager) -> ResourceCreate:
    return update_item(id, data)


@router.delete("/resources/{id}")
def delete(id: int, user: Manager):
    delete_one(id)
