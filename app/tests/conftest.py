import asyncio
import json
from datetime import datetime
from sqlalchemy import select

import pytest
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport

from app.main import app as fastapi_app
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.users.models import Users


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding='utf-8') as f:
            return json.load(f)

    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    bookings = open_mock_json('bookings')
    users = open_mock_json('users')

    for booking in bookings:
        for fname in ('date_from', 'date_to'):
            booking[fname] = datetime.fromisoformat(booking[fname]).date()

    async with async_session_maker() as s:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_booking = insert(Bookings).values(bookings)

        await s.execute(add_hotels)
        await s.execute(add_rooms)
        await s.execute(add_users)
        await s.execute(add_booking)

        await s.commit()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test/",
    ) as client:
        yield client


@pytest.fixture(scope='session')
async def authorized_client():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test/",
    ) as ac:
        email = "test@testtest.com"
        passw = "tests"

        await ac.post(
            "/auth/register",
            json={
                "email": email,
                "password": passw,
            }
        )

        await ac.post(
            "/auth/login",
            json={
                "email": email,
                "password": passw,
            }
        )

        assert ac.cookies.get("booking_access_token") is not None

        yield ac

@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
