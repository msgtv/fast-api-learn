from datetime import date

from app.dao.base import BaseDAO
from app.hotels.models import Hotels


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels_by_location(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ):
        hotels = await super().get_all(location=location)

        return hotels
