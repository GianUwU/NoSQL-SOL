import gridfs
import os
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["jukebox"]
col = db["songs"]
fs = gridfs.GridFS(db)


class Song:
    def __init__(self, name, artist, album=None, genre=None, year=None):
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year


def search_songs(query):
    return list(col.find({"name": {"$regex": query, "$options": "i"}}))


def add_song():
    name = input("Name: ").strip()
    artist = input("Interpret: ").strip()
    album = input("Album (optional): ").strip() or None
    genre = input("Genre (optional): ").strip() or None
    year_in = input("Jahr (optional): ").strip()
    year = int(year_in) if year_in else None

    filepath = input("Pfad zur Audiodatei: ").strip()
    if not os.path.isfile(filepath):
        print("Datei nicht gefunden.")
        return

    with open(filepath, "rb") as f:
        file_id = fs.put(f, filename=os.path.basename(filepath))

    col.insert_one({
        "name": name,
        "artist": artist,
        "album": album,
        "genre": genre,
        "year": year,
        "file_id": file_id
    })
    print("Song gespeichert.")


def edit_song():
    query = input("Song suchen: ").strip()
    results = search_songs(query)
    if not results:
        print("Keine Songs gefunden.")
        return

    for i, r in enumerate(results):
        print(f"{i+1}. {r['name']} - {r['artist']}")

    choice = input("Auswahl: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        print("Ungültige Auswahl.")
        return
    song = results[int(choice) - 1]

    print("Leer lassen = unverändert")
    updates = {}
    for field in ["name", "artist", "album", "genre"]:
        val = input(f"{field} [{song.get(field) or ''}]: ").strip()
        if val:
            updates[field] = val
    year_in = input(f"Jahr [{song.get('year') or ''}]: ").strip()
    if year_in:
        updates["year"] = int(year_in)

    if updates:
        col.update_one({"_id": song["_id"]}, {"$set": updates})
        print("Aktualisiert.")


def delete_song():
    query = input("Song suchen: ").strip()
    results = search_songs(query)
    if not results:
        print("Keine Songs gefunden.")
        return

    for i, r in enumerate(results):
        print(f"{i+1}. {r['name']} - {r['artist']}")

    choice = input("Auswahl: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        print("Ungültige Auswahl.")
        return
    song = results[int(choice) - 1]

    fs.delete(song["file_id"])
    col.delete_one({"_id": song["_id"]})
    print("Song gelöscht.")


while True:
    print("\n1) Song hinzufügen\n2) Song bearbeiten\n3) Song löschen\n4) Beenden")
    c = input("> ").strip()
    if c == "1":
        add_song()
    elif c == "2":
        edit_song()
    elif c == "3":
        delete_song()
    elif c == "4":
        break
