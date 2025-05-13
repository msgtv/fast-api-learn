from typing import List

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: List[str]
    quantity: int
    image_id: int


class SRoomWithLeft(SRoom):
    rooms_left: int
