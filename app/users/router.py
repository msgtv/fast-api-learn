from typing import List

from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExists, IncorrectEmailOrPassword
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_admin_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserInfo
from app.users.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExists()

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
    )

    if user:
        token = create_access_token(
            {"sub": str(user.id)},
        )

        response.set_cookie("booking_access_token", token, httponly=True)
        return {
            'access_token': token,
        }
    raise IncorrectEmailOrPassword()


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {}


@router.get("/me")
async def get_me(user: SUserInfo = Depends(get_current_user)) -> SUserInfo:
    return user

@router.get("/users")
async def get_users(user: Users = Depends(get_admin_user)) -> List[SUserInfo]:
    users = await UsersDAO.get_all()

    return users