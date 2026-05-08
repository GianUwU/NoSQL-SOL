from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["restaurants"]

pipeline = [
    {"$unwind": "$grades"},
    {"$group": {"_id": "$name", "avg_score": {"$avg": "$grades.score"}}},
    {"$sort": {"avg_score": -1}},
    {"$limit": 3}
]

for r in col.aggregate(pipeline):
    print(f"{r['_id']}: {r['avg_score']:.2f}")
