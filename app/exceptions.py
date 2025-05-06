from fastapi import HTTPException, status


UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)


IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)


TokenExpiredError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is expired",
)


TokenAbsentError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is invalid",
)


IncorrectTokenFormatError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token format",
)


UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)
