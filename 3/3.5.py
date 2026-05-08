from pymongo import MongoClient
from datetime import datetime

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
    for i, r in enumerate(results):
        print(f"{i + 1}. {r['name']} | {r['cuisine']} | {r['borough']}")

    if len(results) == 1:
        selected = results[0]
    else:
        while True:
            choice = input("Select (number): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(results):
                selected = results[int(choice) - 1]
                break
            print("Invalid selection.")

    doc_id = selected["_id"]

    score = input(f"Score for '{selected['name']}': ").strip()
    col.update_one(
        {"_id": doc_id},
        {"$push": {"grades": {"date": datetime.now(), "score": int(score)}}}
    )
    print("Rating added.")
