import os
from pymongo import MongoClient

# Connection-String aus Umgebungsvariable lesen
connection_string = os.environ.get("MONGODB_URI")

if not connection_string:
    print("Fehler: Umgebungsvariable MONGODB_URI ist nicht gesetzt.")
    print("Beispiel: export MONGODB_URI='mongodb+srv://user:pass@cluster.mongodb.net/'")
    exit(1)

client = MongoClient(connection_string)

try:
    dbs = client.list_database_names()
    print("Verbindung erfolgreich.")
    print("Datenbanken:", dbs)
except Exception as e:
    print("Verbindung fehlgeschlagen:", e)
