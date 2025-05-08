from fastapi.exceptions import HTTPException


class NoDateSetException(HTTPException):
    status_code = 400

    def __init__(self, date_type):
        super().__init__(
            status_code=self.status_code,
            detail=f'"{date_type}" was not set'
        )


class HotelNotFoundException(HTTPException):
    status_code = 404
    def __init__(self, hotel_id: int):
        super().__init__(
            status_code=self.status_code,
            detail=f'Hotel ID {hotel_id} not found'
        )
