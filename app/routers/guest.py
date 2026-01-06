from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from app.core.security import get_current_user
from app.schemas.guest import GuestCreate, GuestResponse
from app.services.guest import (
    create_guest_service,
    get_guests_service,
    get_guest_service
)

router = APIRouter(prefix="/guests", tags=["Guests"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=GuestResponse)
def create_guest(guest: GuestCreate):
    new_guest = create_guest_service(guest.model_dump())
    return {
        "id": str(new_guest["_id"]),
        "name": new_guest["name"],
        "email": new_guest["email"],
        "phone": new_guest["phone"],
        "id_proof": new_guest["id_proof"]
    }

@router.get("/all", response_model=list[GuestResponse])
def get_guests():
    return [
        {
            "id": g["_id"],
            "name": g["name"],
            "email": g.get("email",""),
            "phone": g["phone"],
            "id_proof": g["id_proof"]
        }
        for g in get_guests_service()
    ]

@router.get("/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: str):
    guest = get_guest_service(guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    return {
        "id": guest["_id"],
        "name": guest["name"],
        "email": guest["email"],
        "phone": guest["phone"],
        "id_proof": guest["id_proof"]
    }
