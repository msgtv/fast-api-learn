from fastapi import HTTPException, status


class UnauthorizedError(HTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED


class UserAlreadyExists(UnauthorizedError):
    detail="User already exists"


class IncorrectEmailOrPassword(UnauthorizedError):
    detail="Incorrect email or password"


class TokenExpiredError(UnauthorizedError):
    detail="Token is expired"


class TokenAbsentError(UnauthorizedError):
    detail="Token is invalid"


class IncorrectTokenFormatError(UnauthorizedError):
    detail="Incorrect token format"
