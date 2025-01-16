from pydantic import BaseModel
from datetime import datetime
from .resources import ResourceDetail
from .user import UserDetail

class BookingCreate(BaseModel):
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime


class BookingDetail(BaseModel):
    user: UserDetail
    resource: ResourceDetail
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    
    