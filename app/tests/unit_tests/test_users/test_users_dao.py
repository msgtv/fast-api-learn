import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email,is_present",
    [
        (1, "fedor@moloko.ru", True),
        (2, "sharik@moloko.ru", True),
        (999, "_", False),
    ]
)
async def test_get_user_by_id(user_id, email, is_present):
    user = await UsersDAO.get_by_id(user_id)

    if is_present:
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
