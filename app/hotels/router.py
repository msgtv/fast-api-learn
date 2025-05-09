from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.hotels.dao import HotelsDAO
from app.hotels.exceptions import NoDateSetException, HotelNotFoundException
from app.hotels.schemas import SHotelWithRoomsLeft, SHotel, SHotelsSearchArgs

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels & Rooms"],
)


@router.get('/{hotel_id}', operation_id='get_hotel_by_id')
async def get_hotel(hotel_id: int) -> SHotel:
    hotel = await HotelsDAO.get_by_id(hotel_id)
    if hotel:
        return hotel
    raise HotelNotFoundException(hotel_id)


@router.get("/{location}")
async def get_hotels_by_location(
        args: SHotelsSearchArgs = Depends(),
) -> List[SHotelWithRoomsLeft|SHotel]:
    if args.date_from and args.date_to:
        hotels = await HotelsDAO.get_hotels_by_location_rooms_left(
            args.location, args.date_from, args.date_to
        )
    elif not (args.date_from or args.date_to):
        hotels = await HotelsDAO.get_hotels_by_location(location=args.location)
    else:
        if not args.date_from:
            raise NoDateSetException(date_type='Date From')
        else:
            raise NoDateSetException(date_type='Date To')

    return hotels
