from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from sqladmin import Admin

from redis import asyncio as aioredis

from app.admin.auth import authentication_backend
from app.config import settings
from app.database import engine
from app.users.router import router as user_router
from app.bookings.router import router as booking_router
from app.hotels.router import router as hotel_router
from app.pages.router import router as page_router
from app.images.router import router as image_router
from app.admin import (
    UserAdmin,
    BookingAdmin,
    RoomAdmin,
    HotelAdmin,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # "redis://:your_redis_password@localhost:6379/0"
    redis = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        username=settings.REDIS_USER,
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotel_router)
# app.include_router(room_router)
app.include_router(page_router)
app.include_router(image_router)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Authorization",
    ],
)


admin = Admin(app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)
