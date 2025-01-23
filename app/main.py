from typing import Annotated
from fastapi import FastAPI, Header, Depends
from .scheemas.user import UserDetail

from .dependencies.auth import get_current_user_name, AdminUser, Employee, Manager
from .api import users, bookings, resources


app = FastAPI()

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(resources.router)


@app.get("/")
def read_items(user: Employee):
    return user
