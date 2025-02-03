from typing import Annotated
from fastapi import FastAPI, Header, Depends
from app.scheemas.user import UserDetail

from app.dependencies.auth import get_current_user_name, AdminUser, Employee, Manager
from app.api import users, bookings, resources
from app.database import get_db_session

from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(resources.router)


@app.get("/")
def read_items(user: Employee):
    return user

