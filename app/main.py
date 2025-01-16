from fastapi import FastAPI, Header

from .api import users, bookings, resources


app = FastAPI()

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(resources.router)



@app.get("/")
def read_items(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}
