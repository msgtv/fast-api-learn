from sqladmin import ModelView

from app.hotels.rooms.models import Rooms


class RoomAdmin(ModelView, model=Rooms):
    name_plural = 'Rooms'
    name = 'Room'
    icon = 'fa-solid fa-bed'

    column_list = [
        "id",
        "hotel",
        "price",
        "quantity",
        "image_id",
    ]
