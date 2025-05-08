from datetime import date

from sqlalchemy import select, insert, delete, and_, or_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        with booked_rooms as (
            select
                *
            from
                bookings
            where
                (
                    room_id = 1
                        and
                    (
                        (date_from >= '2025-05-15' and date_from <= '2025-06-20')
                        or
                        (date_from <= '2025-05-15' and date_to > '2025-05-15')
                    )
                )
        )
        select
            rooms.quantity - COUNT(booked_rooms.room_id) as left_rooms
        from rooms
        left join booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        group by rooms.quantity, booked_rooms.room_id

        :return:
        """

        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            )
                        )
                    )
                ).cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"),
                )
                .select_from(Rooms)
                .join(
                    booked_rooms,
                    Rooms.id == booked_rooms.c.room_id,
                    isouter=True,
                )
                .where(Rooms.id == room_id)
                .group_by(
                    Rooms.quantity,
                    booked_rooms.c.room_id,
                )
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = (
                    select(Rooms.price)
                    .filter_by(id=room_id)
                )

                price = await session.execute(get_price)
                price = price.scalar()

                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)

                await session.commit()

                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete(
            cls,
            user_id: int,
            booking_id: int,
    ):
        async with async_session_maker() as session:
            delete_booking = (
                delete(Bookings)
                .where(
                    and_(
                        Bookings.user_id == user_id,
                        Bookings.id == booking_id,
                    )
                ).returning(Bookings.id)
            )

            deleted_booking = await session.execute(delete_booking)
            deleted_booking = deleted_booking.scalar()

            await session.commit()

            return deleted_booking
