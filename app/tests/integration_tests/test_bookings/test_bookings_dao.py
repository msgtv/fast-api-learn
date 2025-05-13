import pytest
from datetime import datetime

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize(
    "user_id,room_id,date_from,date_to",
    [
        (1, 1, '2025-10-14', '2025-10-24'),
        (2, 1, '2025-10-14', '2025-10-24'),
        (1, 2, '2025-01-14', '2025-02-24'),
        (1, 2, '2025-01-04', '2025-01-24'),
    ]
)
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.fromisoformat(date_from).date()
    date_to = datetime.fromisoformat(date_to).date()

    new_booking = await BookingDAO.add(
        user_id,
        room_id,
        date_from,
        date_to,
    )

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    booking = await BookingDAO.get_by_id(new_booking.id)

    assert booking is not None
