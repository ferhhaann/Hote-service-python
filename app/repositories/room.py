from app.core.database import room_collection
from bson import ObjectId
from bson.errors import InvalidId

def create_room(room_data: dict):
    room_data["status"] = "AVAILABLE"
    result = room_collection.insert_one(room_data)
    room_data["_id"] = result.inserted_id
    return room_data

def get_rooms():
    rooms = []
    for room in room_collection.find():
        room["_id"] = str(room["_id"])
        rooms.append(room)
    return rooms

def get_room_by_id(room_id: str):
    try:
        room = room_collection.find_one({"_id": ObjectId(room_id)})
        if room:
            room["_id"] = str(room["_id"])
        return room
    except InvalidId:
        return None

def get_room_by_number(room_number: str):
    room = room_collection.find_one({"room_number": room_number})
    if room:
        room["_id"] = str(room["_id"])
    return room

def update_room_status(room_id: str, status: str):
    try:
        result = room_collection.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": {"status": status}}
        )
        if result.modified_count == 0:
            return None
        return get_room_by_id(room_id)
    except InvalidId:
        return None