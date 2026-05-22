import psutil
import time
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["power_stats"]["logs"]


class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None:
            self.cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            self.ram_total = ram.total
            self.ram_used = ram.used
            self.timestamp = datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp


print("Logging gestartet... (Ctrl+C zum Beenden)")

while True:
    p = Power()

    col.insert_one({
        "cpu": p.cpu,
        "ram_total": p.ram_total,
        "ram_used": p.ram_used,
        "timestamp": p.timestamp
    })

    count = col.count_documents({})
    if count > 10000:
        to_delete = count - 10000
        oldest = list(col.find({}, {"_id": 1}).sort("timestamp", 1).limit(to_delete))
        ids = [doc["_id"] for doc in oldest]
        col.delete_many({"_id": {"$in": ids}})
