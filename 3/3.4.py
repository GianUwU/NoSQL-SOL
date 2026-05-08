from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["restaurants"]

name = input("Name: ").strip()
cuisine = input("Cuisine: ").strip()

query = {}
if name:
    query["name"] = {"$regex": name, "$options": "i"}
if cuisine:
    query["cuisine"] = {"$regex": cuisine, "$options": "i"}

results = list(col.find(query, {"name": 1, "cuisine": 1, "borough": 1}))

if not results:
    print("No restaurants found.")
else:
    for r in results:
        print(f"{r['name']} | {r['cuisine']} | {r['borough']}")
