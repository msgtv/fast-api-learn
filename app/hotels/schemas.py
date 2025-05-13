from datetime import date, datetime
from typing import List

from fastapi.params import Query
from pydantic import BaseModel, ConfigDict


# class HotelsSearchArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: date,
#             date_to: date,
#             stars: Optional[int] = Query(None, ge=1, le=5),
#             has_spa: Optional[bool] = None,
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa


class SHotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date = Query(None, description=f'Например, {datetime.now().date()}'),
            date_to: date = Query(None, description=f'Например, {datetime.now().date()}'),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to


class SHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int


class SHotelWithRoomsLeft(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int
