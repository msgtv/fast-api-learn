from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.users.router import router as user_router
from app.bookings.router import router as booking_router
from app.hotels.router import router as hotel_router
from app.hotels.rooms.router import router as room_router

app = FastAPI()

app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotel_router)
app.include_router(room_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
