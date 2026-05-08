from pymongo import MongoClient
import math

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["restaurants"]

perigord = col.find_one({"name": "Le Perigord"})
lon1, lat1 = perigord["address"]["coord"]

nearest = None
min_dist = float("inf")

for r in col.find({"name": {"$ne": "Le Perigord"}, "address.coord": {"$exists": True}}):
    coords = r["address"]["coord"]
    if len(coords) == 2:
        d = math.sqrt((lon1 - coords[0]) ** 2 + (lat1 - coords[1]) ** 2)
        if d < min_dist:
            min_dist = d
            nearest = r

print(f"{nearest['name']} | {nearest['address']['street']}, {nearest['address']['zipcode']}")
