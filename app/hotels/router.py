from datetime import date
from typing import List, Optional

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.exceptions import NoDateSetException, HotelNotFoundException
from app.hotels.schemas import SHotelWithRoomsLeft, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels & Rooms"],
)


@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int) -> SHotel:
    hotel = await HotelsDAO.get_by_id(hotel_id)
    if hotel:
        return hotel
    raise HotelNotFoundException(hotel_id)


@router.get("/{location}")
async def get_hotels_by_location(
        location: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
) -> List[SHotelWithRoomsLeft|SHotel]:
    if date_from and date_to:
        hotels = await HotelsDAO.get_hotels_by_location_rooms_left(
            location, date_from, date_to
        )
    elif not (date_from or date_to):
        hotels = await HotelsDAO.get_hotels_by_location(location=location)
    else:
        if not date_from:
            raise NoDateSetException(date_type='Date From')
        else:
            raise NoDateSetException(date_type='Date To')

    return hotels
