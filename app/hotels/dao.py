from datetime import date

from sqlalchemy import select, join, and_, or_, func

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels_by_location_rooms_left(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings WHERE (
                (date_from >= '2023-06-15' AND date_from <= '2023-06-30')
                OR
                (date_from <= '2023-06-15' AND date_to > '2023-06-15')
            )
        )

        SELECT
            hotels.id,
            hotels.name,
            hotels.location,
            hotels.services,
            hotels.rooms_quantity,
            hotels.image_id,
            hotels.rooms_quantity - count(booked_rooms.room_id) AS rooms_left
        FROM rooms
        JOIN
            hotels ON hotels.id = rooms.hotel_id
        LEFT JOIN
            booked_rooms ON booked_rooms.room_id = rooms.id
        GROUP BY hotels.id
        ORDER BY hotels.id
        """

        async with async_session_maker() as session:
            get_booked_rooms = (
                select(Bookings)
                .where(
                    or_(
                        and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                        and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                    )
                ).cte("booked_rooms")
            )

            get_hotels_with_rooms_left = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    (Hotels.rooms_quantity - func.count(get_booked_rooms.c.room_id)).label("rooms_left"),
                )
                .select_from(Hotels)
                .join(Rooms, Hotels.id == Rooms.hotel_id)
                .join(get_booked_rooms, Rooms.id == get_booked_rooms.c.room_id, isouter=True)
                .where(Hotels.location.icontains(location))
                .group_by(
                    Hotels.id
                )
                .order_by(Hotels.id)
            )

            hotels_with_rooms_left = await session.execute(get_hotels_with_rooms_left)
            hotels_with_rooms_left = hotels_with_rooms_left.mappings().all()

            return hotels_with_rooms_left


    @classmethod
    async def get_hotels_by_location(
            cls,
            location: str,
    ):
        async with async_session_maker() as session:
            get_hotels = (
                select(Hotels)
                .where(Hotels.location.icontains(location))
            )

            hotels = await session.execute(get_hotels)
            hotels = hotels.scalars().all()

            return hotels
