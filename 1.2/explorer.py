from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
except (ConnectionFailure, ServerSelectionTimeoutError):
    print("Verbindung zur Datenbank fehlgeschlagen.")
    exit(1)


def main():
    while True:
        try:
            dbs = client.list_database_names()
        except Exception as e:
            print(f"Fehler beim Laden der Datenbanken: {e}")
            input("\nPress any button to return")
            continue

        print("Databases")
        if not dbs:
            print("No Database")
            input("\nPress any button to return")
            continue
        for db in dbs:
            print(f" - {db}")

        while True:
            db_name = input("\nSelect Database: ").strip()
            if db_name in dbs:
                break
            print("Database not found.")

        try:
            cols = client[db_name].list_collection_names()
        except Exception as e:
            print(f"Fehler beim Laden der Collections: {e}")
            input("\nPress any button to return")
            continue

        print(f"\n{db_name}\n")
        print("Collections")
        if not cols:
            print("No Collection")
            input("\nPress any button to return")
            continue
        for col in cols:
            print(f" - {col}")

        while True:
            col_name = input("\nSelect Collection: ").strip()
            if col_name in cols:
                break
            print("Collection not found.")

        try:
            docs = list(client[db_name][col_name].find({}, {"_id": 1}))
        except Exception as e:
            print(f"Fehler beim Laden der Documents: {e}")
            input("\nPress any button to return")
            continue

        print(f"\n{db_name}.{col_name}\n")
        print("Documents")
        if not docs:
            print("No Document")
            input("\nPress any button to return")
            continue
        for doc in docs:
            print(f" - {doc['_id']}")

        doc_ids = {str(doc["_id"]): doc["_id"] for doc in docs}
        while True:
            doc_input = input("\nSelect Document: ").strip()
            if doc_input in doc_ids:
                break
            print("Document not found.")

        try:
            doc = client[db_name][col_name].find_one({"_id": doc_ids[doc_input]})
        except Exception as e:
            print(f"Fehler beim Laden des Documents: {e}")
            input("\nPress any button to return")
            continue

        print(f"\n{db_name}.{col_name}.{doc_input}\n")
        for key, value in doc.items():
            if key != "_id":
                print(f"{key}: {value}")

        input("\nPress any button to return")


main()
