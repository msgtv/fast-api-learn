from datetime import date
from typing import List

from app.hotels.exceptions import NoDateSetException
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomWithLeft, SRoom
from app.hotels.router import router


# TODO: route на получение списка комнат по отелю
@router.get('/{hotel_id}/rooms')
async def get_rooms(
        hotel_id: int,
        date_from: date = None,
        date_to: date = None,
) -> List[SRoom|SRoomWithLeft]:
    if date_from and date_to:
        rooms = await RoomsDAO.get_rooms_with_left(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
    elif not (date_from or date_to):
        rooms = await RoomsDAO.get_all(hotel_id=hotel_id)
    else:
        if not date_from:
            raise NoDateSetException(date_type='Date From')
        else:
            raise NoDateSetException(date_type='Date To')

    return rooms
