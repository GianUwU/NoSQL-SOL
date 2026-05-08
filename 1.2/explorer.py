from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


def main():
    while True:
        dbs = client.list_database_names()

        print("Databases")
        if not dbs:
            print("No Database")
            input("\nPress any button to return")
            continue
        for db in dbs:
            print(f" - {db}")

        db_name = input("\nSelect Database: ").strip()
        if db_name not in dbs:
            print("Database not found.")
            continue

        cols = client[db_name].list_collection_names()

        print(f"\n{db_name}\n")
        print("Collections")
        if not cols:
            print("No Collection")
            input("\nPress any button to return")
            continue
        for col in cols:
            print(f" - {col}")

        col_name = input("\nSelect Collection: ").strip()
        if col_name not in cols:
            print("Collection not found.")
            continue

        docs = list(client[db_name][col_name].find({}, {"_id": 1}))

        print(f"\n{db_name}.{col_name}\n")
        print("Documents")
        if not docs:
            print("No Document")
            input("\nPress any button to return")
            continue
        for doc in docs:
            print(f" - {doc['_id']}")

        doc_input = input("\nSelect Document: ").strip()
        doc_ids = {str(doc["_id"]): doc["_id"] for doc in docs}
        if doc_input not in doc_ids:
            print("Document not found.")
            continue

        doc = client[db_name][col_name].find_one({"_id": doc_ids[doc_input]})

        print(f"\n{db_name}.{col_name}.{doc_input}\n")
        for key, value in doc.items():
            if key != "_id":
                print(f"{key}: {value}")

        input("\nPress any button to return")


main()
