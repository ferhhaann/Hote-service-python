from datetime import date, datetime
from app.repositories.reservation import (
    create_reservation,
    get_active_reservations,
    get_reservations_for_room,
    get_reservation_by_id,
    update_reservation_status
)
from app.repositories.room import get_room_by_id, get_room_by_number, update_room_status
from app.repositories.guest import (
    get_guest_by_id,
    get_guest_by_phone,
    get_guest_by_id_proof,
    create_guest
)

def is_room_available(room_id: str, check_in, check_out):
    reservations = get_reservations_for_room(room_id)

    # Convert check_in and check_out to datetime if they are date objects
    if isinstance(check_in, date) and not isinstance(check_in, datetime):
        check_in = datetime.combine(check_in, datetime.min.time())
    if isinstance(check_out, date) and not isinstance(check_out, datetime):
        check_out = datetime.combine(check_out, datetime.min.time())

    for r in reservations:
        if r["status"] in ["BOOKED", "CHECKED_IN"]:
            # Handle both date and datetime objects from database
            res_check_in = r["check_in_date"]
            res_check_out = r["check_out_date"]
            
            if isinstance(res_check_in, date) and not isinstance(res_check_in, datetime):
                res_check_in = datetime.combine(res_check_in, datetime.min.time())
            if isinstance(res_check_out, date) and not isinstance(res_check_out, datetime):
                res_check_out = datetime.combine(res_check_out, datetime.min.time())
            
            if res_check_in < check_out and res_check_out > check_in:
                return False
    return True

def create_reservation_service(data: dict):
    # Find room by room number
    room = get_room_by_number(data["room_number"])
    if not room:
        raise Exception("Room not found")
    
    room_id = room["_id"]

    # Check if guest exists by phone or id_proof
    guest = get_guest_by_phone(data["phone_number"])
    if not guest:
        guest = get_guest_by_id_proof(data["id_proof"])
    
    # If guest doesn't exist, create new guest
    if not guest:
        guest_data = {
            "name": data["guest_name"],
            "phone": data["phone_number"],
            "id_proof": data["id_proof"],
        }
        guest = create_guest(guest_data)
    
    guest_id = str(guest["_id"])

    # Validate dates
    if data["check_out_date"] <= data["check_in_date"]:
        raise Exception("Invalid date range")

    # Check availability
    if not is_room_available(
        room_id,
        data["check_in_date"],
        data["check_out_date"]
    ):
        raise Exception("Room not available")

    # Convert date objects to datetime for MongoDB
    check_in_datetime = datetime.combine(data["check_in_date"], datetime.min.time())
    check_out_datetime = datetime.combine(data["check_out_date"], datetime.min.time())

    reservation_data = {
        "guest_id": guest_id,
        "guest_name": guest["name"],
        "guest_phone": guest["phone"],
        "guest_email": guest.get("email", ""),
        "guest_id_proof": guest["id_proof"],
        "room_id": room_id,
        "check_in_date": check_in_datetime,
        "check_out_date": check_out_datetime,
        "status": "BOOKED"
    }
    return create_reservation(reservation_data)

def check_in_service(reservation_id: str):
    reservation = get_reservation_by_id(reservation_id)

    if not reservation:
        raise Exception("Reservation not found")

    if reservation["status"] != "BOOKED":
        raise Exception("Cannot check-in")

    update_reservation_status(reservation_id, "CHECKED_IN")
    
    # Update room status to OCCUPIED
    update_room_status(reservation["room_id"], "OCCUPIED")

def check_out_service(reservation_id: str):
    reservation = get_reservation_by_id(reservation_id)

    if not reservation:
        raise Exception("Reservation not found")

    if reservation["status"] != "CHECKED_IN":
        raise Exception("Cannot check-out")

    update_reservation_status(reservation_id, "CHECKED_OUT")
    
    # Update room status back to AVAILABLE
    update_room_status(reservation["room_id"], "AVAILABLE")

def walk_in_reservation_service(data: dict):
    """
    Handle walk-in reservations with custom pricing
    Supports both existing and new guests
    """
    guest_info = data["guest"]
    
    # Handle existing guest
    if guest_info.get("guest_id"):
        guest = get_guest_by_id(guest_info["guest_id"])
        if not guest:
            raise Exception("Guest not found")
    # Handle new guest
    else:
        if not all([guest_info.get("name"), guest_info.get("phone"), guest_info.get("id_proof")]):
            raise Exception("Name, phone, and id_proof are required for new guest")
        
        # Check if guest already exists by phone or id_proof
        guest = get_guest_by_phone(guest_info["phone"])
        if not guest:
            guest = get_guest_by_id_proof(guest_info["id_proof"])
        
        # Create new guest if doesn't exist
        if not guest:
            guest_data = {
                "name": guest_info["name"],
                "phone": guest_info["phone"],
                "id_proof": guest_info["id_proof"]
            }
            guest = create_guest(guest_data)
    
    guest_id = str(guest["_id"])
    
    # Get room
    room = get_room_by_id(data["room_id"])
    if not room:
        raise Exception("Room not found")
    
    # Validate dates
    check_in = data["check_in_date"]
    check_out = data["check_out_date"]
    
    if check_out <= check_in:
        raise Exception("Check-out date must be after check-in date")
    
    # Check room availability
    if not is_room_available(data["room_id"], check_in, check_out):
        raise Exception("Room not available for selected dates")
    
    # Convert date objects to datetime for MongoDB
    check_in_datetime = datetime.combine(check_in, datetime.min.time())
    check_out_datetime = datetime.combine(check_out, datetime.min.time())
    
    # Create reservation with custom pricing and guest details
    reservation_data = {
        "guest_id": guest_id,
        "guest_name": guest["name"],
        "guest_phone": guest["phone"],
        "guest_email": guest.get("email", ""),
        "guest_id_proof": guest["id_proof"],
        "room_id": data["room_id"],
        "check_in_date": check_in_datetime,
        "check_out_date": check_out_datetime,
        "total_amount": data["total_amount"],
        "price_per_night": data["price_per_night"],
        "status": "CHECKED_IN"  # Walk-in is immediately checked in
    }
    
    reservation = create_reservation(reservation_data)
    
    # Update room status from payload
    update_room_status(data["room_id"], data["room_status"])
    
    return reservation

def get_active_reservations_service():
    return get_active_reservations()

def get_reservations_by_room_service(room_id: str):
    """Get all reservations for a specific room"""
    return get_reservations_for_room(room_id)
