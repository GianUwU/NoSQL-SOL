import gridfs
import tempfile
import os
import pygame
from pymongo import MongoClient
from collections import deque

client = MongoClient("mongodb://localhost:27017/")
db = client["jukebox"]
col = db["songs"]
fs = gridfs.GridFS(db)

pygame.mixer.init()
playlist = deque()


def search():
    name = input("Name: ").strip()
    artist = input("Interpret: ").strip()
    album = input("Album: ").strip()
    genre = input("Genre: ").strip()

    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if artist:
        query["artist"] = {"$regex": artist, "$options": "i"}
    if album:
        query["album"] = {"$regex": album, "$options": "i"}
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}

    return list(col.find(query))


def play_song(song):
    audio = fs.get(song["file_id"])
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(audio.read())
    tmp.close()

    pygame.mixer.music.load(tmp.name)
    pygame.mixer.music.play()
    print(f"Spielt: {song['name']} - {song['artist']}")
    input("Enter zum Beenden...")
    pygame.mixer.music.stop()
    os.unlink(tmp.name)


while True:
    print("\n1) Suchen & zur Playlist hinzufügen")
    print("2) Abspielen")
    print("3) Playlist anzeigen")
    print("4) Beenden")
    c = input("> ").strip()

    if c == "1":
        results = search()
        if not results:
            print("Keine Songs gefunden.")
            continue
        for i, r in enumerate(results):
            print(f"{i+1}. {r['name']} - {r['artist']}")
        choice = input("Zur Playlist hinzufügen (Nummer): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            song = results[int(choice) - 1]
            playlist.append(song)
            print(f"'{song['name']}' hinzugefügt.")

    elif c == "2":
        if playlist:
            song = playlist.popleft()
        else:
            total = col.count_documents({})
            if total == 0:
                print("Keine Songs in der Datenbank.")
                continue
            song = list(col.aggregate([{"$sample": {"size": 1}}]))[0]
            print(f"Zufälliger Song: {song['name']} - {song['artist']}")
        play_song(song)

    elif c == "3":
        if not playlist:
            print("Playlist ist leer.")
        else:
            for i, s in enumerate(playlist):
                print(f"{i+1}. {s['name']} - {s['artist']}")

    elif c == "4":
        break
