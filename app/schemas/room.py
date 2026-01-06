from pydantic import BaseModel
from typing import Literal

class RoomCreate(BaseModel):
    room_number: str
    type: Literal["STANDARD", "DELUXE", "PREMIUM"]

class RoomResponse(BaseModel):
    id: str
    room_number: str
    type: str
    status: str
