from sqladmin import ModelView
from sqlalchemy.orm import relationship

from app.bookings.models import Bookings


class BookingAdmin(ModelView, model=Bookings):
    name = "Bookings"
    name_plural = "Bookings"
    icon = 'fa-solid fa-book'

    column_list = [
        "id",
        "room_id",
        "user",
        "date_from",
        "date_to",
        "price",
        "total_days",
        "total_cost",
    ]
