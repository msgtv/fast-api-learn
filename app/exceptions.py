from fastapi import HTTPException, status


class UnauthorizedError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExists(UnauthorizedError):
    detail = "User already exists"


class IncorrectEmailOrPassword(UnauthorizedError):
    detail="Incorrect email or password"


class TokenExpiredError(UnauthorizedError):
    detail="Token is expired"


class TokenAbsentError(UnauthorizedError):
    detail="Token is invalid"


class IncorrectTokenFormatError(UnauthorizedError):
    detail="Incorrect token format"


class RoomCannotBooked(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Rooms not left")
