from datetime import date
from typing import List

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels & Rooms"],
)


# TODO: 1. route на получение списка отелей по location
#  2. route на получение всей информации по id отеля

@router.get("/{location}")
async def get_hotels_by_location(
        location: str,
        date_from: date = None,
        date_to: date = None,
) -> List[SHotel]:
    hotels = await HotelsDAO.get_hotels(location, date_from, date_to)

    return hotels
