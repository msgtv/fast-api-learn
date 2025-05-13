import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("pushkin@kolotushkin.com", 'pushkin', 200),
        ("pushkin@kolotushkin.com", 'pushkin', 401),
        ("qwerty", "qwerty", 422)
    ]
)
async def test_register_user(email, password, status_code, ac: AsyncClient) -> None:
    res = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )

    assert res.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test1@example.com", "test", 200),
        ("test1@example.com", "test123", 401),
    ]
)
async def test_login_user(email, password, status_code, ac: AsyncClient) -> None:
    res = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )

    assert res.status_code == status_code
