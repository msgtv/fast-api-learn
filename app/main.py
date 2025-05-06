from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.users.router import router as user_router
from app.bookings.router import router as booking_router

app = FastAPI()

app.include_router(user_router)
app.include_router(booking_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            stars: Optional[int] = Query(None, ge=1, le=5),
            has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


class SHotel(BaseModel):
    address: str
    name: str
    stars: int
    has_spa: bool


@app.get("/hotels")
def get_hotels(
        args: HotelsSearchArgs = Depends(),
) -> list[SHotel]:
    hotels = [
        {
            "address": "ul 1",
            "name": "hotel name",
            "stars": '12',
            "has_spa": '1',
        },
    ]

    return hotels


@app.get("/hotels/{location}")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
):
    if location.lower() == 'moscow':
        return [
            {
                "dates": {
                    "from": date_from,
                    "to": date_to,
                }
            },
            'Russia',
            'Crime',
            'Sova',
        ]

    return f"Not hotels found on {location}"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
