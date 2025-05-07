from fastapi import status
from fastapi.exceptions import HTTPException


class RoomCannotBooked(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Rooms not left")
