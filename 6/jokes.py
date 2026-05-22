from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
col = client["jokes"]["jokes"]


class Joke:
    def __init__(self, text, category, author):
        self.text = text
        self.category = category  # Liste von Kategorien
        self.author = author


class JokeDAO:
    def insert(self, joke):
        col.insert_one({
            "text": joke.text,
            "category": joke.category,
            "author": joke.author
        })

    def get_category(self, category):
        return list(col.find({"category": category}))

    def delete(self, id):
        col.delete_one({"_id": ObjectId(id)})


dao = JokeDAO()

while True:
    print("\n1) Witz hinzufügen")
    print("2) Witze nach Kategorie suchen")
    print("3) Witz löschen")
    print("4) Beenden")
    choice = input("> ").strip()

    if choice == "1":
        text = input("Text: ").strip()
        author = input("Autor: ").strip()
        cats = input("Kategorien (kommagetrennt): ").strip()
        category = [c.strip() for c in cats.split(",")]
        dao.insert(Joke(text, category, author))
        print("Witz gespeichert.")

    elif choice == "2":
        cat = input("Kategorie: ").strip()
        jokes = dao.get_category(cat)
        if not jokes:
            print("Keine Witze in dieser Kategorie.")
        for j in jokes:
            print(f"\n[{j['_id']}] {j['text']}  (von {j['author']})")

    elif choice == "3":
        id_input = input("ID des Witzes: ").strip()
        dao.delete(id_input)
        print("Gelöscht.")

    elif choice == "4":
        break
