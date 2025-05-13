import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code",
    [
        *[(4, "2025-10-14","2025-10-24", 200)] * 8,
        (4, "2025-10-14","2025-10-24", 409)
    ]
)
async def test_add_and_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        authorized_client: AsyncClient
):
    response = await authorized_client.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code

