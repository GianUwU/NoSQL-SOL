from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

client = MongoClient("mongodb://localhost:27017/")
col = client["power_stats"]["logs"]

# letzte 200 Einträge laden
docs = list(col.find({}, {"cpu": 1, "ram_used": 1, "ram_total": 1, "timestamp": 1})
            .sort("timestamp", -1).limit(200))
docs.reverse()

if not docs:
    print("Keine Daten vorhanden. Zuerst power.py starten.")
    exit()

timestamps = [d["timestamp"] for d in docs]
cpu_vals = [d["cpu"] for d in docs]
ram_used_gb = [d["ram_used"] / (1024 ** 3) for d in docs]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

ax1.plot(timestamps, cpu_vals, color="steelblue")
ax1.set_ylabel("CPU (%)")
ax1.set_title("CPU Auslastung")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
fig.autofmt_xdate()

ax2.plot(timestamps, ram_used_gb, color="tomato")
ax2.set_ylabel("RAM (GB)")
ax2.set_title("RAM Auslastung")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
fig.autofmt_xdate()

plt.tight_layout()
plt.show()
