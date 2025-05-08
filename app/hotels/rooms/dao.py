from datetime import date

from sqlalchemy import or_, and_, select, func

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_with_left(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        получить данные по номерам отеля и количество свободных номеров

        SQL⤵
        WITH hotel_rooms AS (
            SELECT id FROM rooms WHERE hotel_id = 1
            ),
            booked_rooms AS (
            SELECT room_id
            FROM bookings
            WHERE
                (
                    room_id IN (SELECT id FROM hotel_rooms)
                    AND (
                    (date_from >= '2023-06-10' AND date_from <= '2023-06-21')
                      OR
                    (date_from <= '2023-06-10' AND date_to > '2023-06-21')
                    )
                )
            )

        SELECT
            id,
            hotel_id,
            name,
            description,
            price,
            services,
            quantity,
            image_id,
            quantity - count(booked_rooms.room_id)
        FROM rooms
        LEFT JOIN
            booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE hotel_id = 1
        GROUP BY id
        """
        async with async_session_maker() as session:
            # получить номера отеля
            get_hotel_rooms = (
                select(Rooms.id)
                .select_from(Rooms)
                .where(Rooms.hotel_id == hotel_id)
                .cte('hotel_rooms')
            )

            # получить занятые номера и их количество
            get_booked_rooms = (
                select(Bookings.room_id)
                .select_from(Bookings)
                .where(
                    and_(
                        Bookings.room_id.in_(
                            select(get_hotel_rooms.c.id)
                        ),
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                        )
                    )
                ).cte('booked_rooms')
            )

            # получить данные по номерам отеля и количество свободных номеров
            get_rooms = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.price,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                    (Rooms.quantity - func.count(get_booked_rooms.c.room_id)).label('rooms_left')
                )
                .select_from(Rooms)
                .join(get_booked_rooms, get_booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.hotel_id == hotel_id)
                .group_by(Rooms.id)
            )

            rooms = await session.execute(get_rooms)
            rooms = rooms.mappings().all()

            return rooms
