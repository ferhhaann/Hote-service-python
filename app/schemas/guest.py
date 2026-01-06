from typing import Optional
from pydantic import BaseModel, EmailStr

class GuestCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    id_proof: str   # Passport / Emirates ID / Aadhaar etc.

class GuestResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    id_proof: Optional[str] = None
