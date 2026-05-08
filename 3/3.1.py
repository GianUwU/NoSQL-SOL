from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["restaurants"]

boroughs = col.distinct("borough")
for b in boroughs:
    print(b)
