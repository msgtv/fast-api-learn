from pydantic import BaseModel, EmailStr

class SUserInfo(BaseModel):
    email: EmailStr

class SUserAuth(SUserInfo):
    password: str
