from datetime import date

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
