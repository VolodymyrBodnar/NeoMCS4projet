from sqlalchemy import event

from models.models import User, Booking, Resource
from database import SessionLocal
from datetime import datetime

session = SessionLocal()


user = User()
user.name = "John"
user.email = '3123213213'


screen = Resource()
screen.name = 'screen'
screen.description = '3123123123213'


book1 = Booking()
book1.user = user
book1.resource = screen

book1.start_time = datetime.now()
book1.end_time = datetime(2025,2,2)


# session.add(user)
# session.add(screen)
# session.add(book1)
# session.commit()



# Всі записи
all = session.query(Booking).all()
for booking in all:
    print(booking.created_at)
