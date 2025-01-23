from ..scheemas.user import UserDetail
from ..scheemas.resources import ResourceDetail
from ..scheemas.booking import BookingCreate, BookingDetail

from .resources import get_item_from_db
from .user import get_user

from datetime import datetime


def get_booking_from_db(id):
    return BookingDetail(
        id=121,
        resource=get_item_from_db(212),
        user=get_user(34234),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        start_time=datetime.now(),
        end_time=datetime.now(),
    )


def create_booking(booking: BookingCreate):
    print(booking)


def get_booking(id: int) -> BookingDetail:
    return get_booking_from_db(id)
