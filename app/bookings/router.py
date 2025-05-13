from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException
import pydantic
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.bookings.exceptions import RoomCannotBooked
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.tasks.tasks import send_confirmation_email

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBooking]:
    bookings = await BookingDAO.get_all(user_id=user.id)

    return bookings


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
) -> SBooking:
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )

    if booking is None:
        raise RoomCannotBooked()

    booking_data = pydantic.TypeAdapter(SBooking).validate_python(booking).model_dump(mode='json')

    send_confirmation_email.delay(booking_data, user.email)

    return booking


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user),
):
    deleted_booking = await BookingDAO.delete(
        user_id=user.id,
        booking_id=booking_id,
    )

    if deleted_booking:
        return Response(status_code=204)
    raise HTTPException(status_code=404)