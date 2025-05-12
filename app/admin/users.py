from sqladmin import ModelView

from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [
        "id",
        "email",
    ]

    column_details_exclude_list = ["hashed_password"]

    can_delete = False