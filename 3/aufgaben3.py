from pymongo import MongoClient
from datetime import datetime
import math

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["restaurants"]


def task_3_1():
    print("=== 3.1 Stadtbezirke ===")
    for b in col.distinct("borough"):
        print(f" - {b}")


def task_3_2():
    print("=== 3.2 Top 3 Restaurants (Durchschnitt Score) ===")
    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {"_id": "$name", "avg_score": {"$avg": "$grades.score"}}},
        {"$sort": {"avg_score": -1}},
        {"$limit": 3}
    ]
    for r in col.aggregate(pipeline):
        print(f" - {r['_id']}: {r['avg_score']:.2f}")


def task_3_3():
    print("=== 3.3 Nächstes Restaurant zu Le Perigord ===")
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

    print(f" - {nearest['name']} | {nearest['address']['street']}, {nearest['address']['zipcode']}")


def task_3_4_and_3_5():
    print("=== 3.4 / 3.5 Restaurant suchen & bewerten ===")
    name = input("Name: ").strip()
    cuisine = input("Küche: ").strip()

    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if cuisine:
        query["cuisine"] = {"$regex": cuisine, "$options": "i"}

    results = list(col.find(query, {"name": 1, "cuisine": 1, "borough": 1}))

    if not results:
        print("Keine Restaurants gefunden.")
        return

    for i, r in enumerate(results):
        print(f"{i + 1}. {r['name']} | {r['cuisine']} | {r['borough']}")

    if len(results) == 1:
        selected = results[0]
    else:
        while True:
            choice = input("Auswahl (Nummer): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(results):
                selected = results[int(choice) - 1]
                break
            print("Ungültige Auswahl.")

    doc_id = selected["_id"]

    score = input(f"Bewertung für '{selected['name']}': ").strip()
    col.update_one(
        {"_id": doc_id},
        {"$push": {"grades": {"date": datetime.now(), "score": int(score)}}}
    )
    print("Bewertung gespeichert.")


print("1) Stadtbezirke")
print("2) Top 3 Restaurants")
print("3) Nächstes zu Le Perigord")
print("4) Restaurant suchen")
print("5) Restaurant suchen & bewerten")

choice = input("\nAufgabe wählen: ").strip()

if choice == "1":
    task_3_1()
elif choice == "2":
    task_3_2()
elif choice == "3":
    task_3_3()
elif choice == "4":
    task_3_4_and_3_5()
elif choice == "5":
    task_3_4_and_3_5()
else:
    print("Ungültige Auswahl.")
