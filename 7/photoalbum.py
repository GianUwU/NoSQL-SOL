import gridfs
import os
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["photoalbum"]
fs = gridfs.GridFS(db)


def add_photo(filepath, album):
    if not os.path.isfile(filepath):
        print("Datei nicht gefunden.")
        return
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_id = fs.put(f, filename=filename, metadata={"album": album})
    print(f"'{filename}' zu Album '{album}' hinzugefügt (ID: {file_id})")


def download_album(album, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = list(db.fs.files.find({"metadata.album": album}))
    if not files:
        print("Keine Bilder in diesem Album gefunden.")
        return
    for file_doc in files:
        data = fs.get(file_doc["_id"])
        save_path = os.path.join(output_dir, file_doc["filename"])
        with open(save_path, "wb") as f:
            f.write(data.read())
        print(f"  {file_doc['filename']} heruntergeladen")
    print(f"{len(files)} Foto(s) gespeichert in '{output_dir}'")


while True:
    print("\n1) Foto hinzufügen")
    print("2) Album herunterladen")
    print("3) Beenden")
    choice = input("> ").strip()

    if choice == "1":
        path = input("Bildpfad: ").strip()
        album = input("Albumname: ").strip()
        add_photo(path, album)

    elif choice == "2":
        album = input("Albumname: ").strip()
        out = input("Ausgabeordner: ").strip()
        download_album(album, out)

    elif choice == "3":
        break
