from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReservationCreate(BaseModel):
    room_number: str
    guest_name: str
    phone_number: str
    id_proof: str
    check_in_date: date
    check_out_date: date

class GuestInfo(BaseModel):
    guest_id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    id_proof: Optional[str] = None

class WalkInReservation(BaseModel):
    guest: GuestInfo
    room_id: str
    check_in_date: date
    check_out_date: date
    total_amount: float
    price_per_night: float
    room_status: str

class ReservationResponse(BaseModel):
    id: str
    guest_name: str
    room_number: str
    phone_number: str
    check_in_date: date
    check_out_date: date
    status: str

class ReservationDetailResponse(BaseModel):
    id: str
    guest_id: str
    guest_name: str
    guest_phone: str
    guest_email: str
    guest_id_proof: str
    room_id: str
    room_number: str
    check_in_date: date
    check_out_date: date
    total_amount: Optional[float] = None
    price_per_night: Optional[float] = None
    status: str