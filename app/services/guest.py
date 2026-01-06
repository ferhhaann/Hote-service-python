from app.repositories.guest import (
    create_guest,
    get_guests,
    get_guest_by_id
)

def create_guest_service(guest_data: dict):
    return create_guest(guest_data)

def get_guests_service():
    return get_guests()

def get_guest_service(guest_id: str):
    return get_guest_by_id(guest_id)
