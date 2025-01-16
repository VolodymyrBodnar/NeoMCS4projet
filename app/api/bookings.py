from fastapi import APIRouter

from ..services.booking import create_booking, get_booking
from ..scheemas.booking import BookingCreate, BookingDetail

router = APIRouter()


@router.get("/booking/{booking_id}")
def retriewe_booking(booking_id: int) -> BookingDetail:
    return get_booking(booking_id)    
