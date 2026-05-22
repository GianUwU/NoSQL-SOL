from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
col = client["rooms"]["rooms"]


class Room:
    def __init__(self, name, capacity, floor):
        self.name = name
        self.capacity = capacity
        self.floor = floor


class Dao_room:
    def insert(self, room):
        result = col.insert_one({
            "name": room.name,
            "capacity": room.capacity,
            "floor": room.floor
        })
        return result.inserted_id

    def get_all(self):
        return list(col.find())

    def update(self, id, data):
        col.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, id):
        col.delete_one({"_id": ObjectId(id)})


# Test
dao = Dao_room()
new_id = dao.insert(Room("A101", 30, 1))
print("Inserted:", new_id)

all_rooms = dao.get_all()
for r in all_rooms:
    print(r)

dao.update(str(new_id), {"capacity": 35})
print("Updated capacity to 35")

dao.delete(str(new_id))
print("Deleted")
