from datetime import datetime

from fastapi import Request, HTTPException, status
from fastapi.params import Depends
from jose import JWTError, jwt

from app.config import settings
from app.users.exceptions import TokenExpiredError, TokenAbsentError, IncorrectTokenFormatError, UnauthorizedError
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentError

    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
    except JWTError:
        raise IncorrectTokenFormatError()

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredError()

    user_id: str = payload.get("sub")
    if not user_id:
        raise UnauthorizedError()

    user = await UsersDAO.get_by_id(int(user_id))
    if not user:
        raise UnauthorizedError()

    return user


async def get_admin_user(user: Users = Depends(get_current_user)):
    # if user.role == 'admin':
    #     return user

    return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

