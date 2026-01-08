from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from app.core.security import get_current_user, require_role
from app.schemas.room import RoomCreate, RoomResponse, StatusUpdate
from app.services.room import (
    create_room_service,
    get_rooms_service,
    get_room_service,
    update_room_status_service
)

router = APIRouter(prefix="/rooms", tags=["Rooms"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=RoomResponse, dependencies=[Depends(require_role("ADMIN"))])
def create_room(room: RoomCreate):
    new_room = create_room_service(room.dict(), ) 
    return {
        "id": str(new_room["_id"]),
        "room_number": new_room["room_number"],
        "type": new_room["type"],
        "status": new_room["status"]
    }

@router.get("/", response_model=list[RoomResponse])
def get_rooms():
    return [
        {
            "id": room["_id"],
            "room_number": room["room_number"],
            "type": room["type"],
            "status": room["status"]
        }
        for room in get_rooms_service()
    ]

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: str):
    room = get_room_service(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return {
        "id": room["_id"],
        "room_number": room["room_number"],
        "type": room["type"],
        "status": room["status"]
    }
@router.put("/{room_id}/status", response_model=RoomResponse)
def update_room_status(room_id: str, payload: StatusUpdate):
    room = get_room_service(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    updated_room = update_room_status_service(room_id, payload.status)
    return {
        "id": updated_room["_id"],
        "room_number": updated_room["room_number"],
        "type": updated_room["type"],
        "status": updated_room["status"]
    }