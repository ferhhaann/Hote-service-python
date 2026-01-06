from app.repositories.room import (
    create_room,
    get_rooms,
    get_room_by_id,
    update_room_status
)

def create_room_service(room_data: dict):
    return create_room(room_data)

def get_rooms_service():
    return get_rooms()

def get_room_service(room_id: str):
    return get_room_by_id(room_id)

def update_room_status_service(room_id: str, status: str):
    return update_room_status(room_id, status)