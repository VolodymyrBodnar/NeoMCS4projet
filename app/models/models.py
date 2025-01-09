from database import Base, engine

from models.booking import Booking
from models.resources import Resource
from models.users import User


# Створення таблиці у базі
Base.metadata.create_all(engine)
