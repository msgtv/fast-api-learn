from sqladmin import ModelView
from app.hotels.models import Hotels


class HotelAdmin(ModelView, model=Hotels):
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"

    column_list = [
        "id",
        "name",
        "location",
        "room_quantity",
        "image_id",
    ]
