from app.core.database import db
from bson import ObjectId
from bson.errors import InvalidId

reservation_collection = db["reservations"]

def create_reservation(data: dict):
    result = reservation_collection.insert_one(data)
    data["_id"] = result.inserted_id
    return data

def get_reservation_by_id(reservation_id: str):
    try:
        reservation = reservation_collection.find_one(
            {"_id": ObjectId(reservation_id)}
        )
        if reservation:
            reservation["_id"] = str(reservation["_id"])
        return reservation
    except InvalidId:
        return None

def get_reservations_for_room(room_id: str):
    return list(
        reservation_collection.find({"room_id": room_id})
    )

def update_reservation_status(reservation_id: str, status: str):
    try:
        result = reservation_collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
    except InvalidId:
        return False

def get_active_reservations():
    return list(
        reservation_collection.find({"status": "BOOKED"})
    )