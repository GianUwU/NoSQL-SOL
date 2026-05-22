import gridfs
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["gridfs_demo"]
fs = gridfs.GridFS(db)


def save_file(filepath):
    filename = filepath.split("/")[-1]
    with open(filepath, "rb") as f:
        file_id = fs.put(f, filename=filename)
    print(f"Datei gespeichert. ID: {file_id}")
    return file_id


def restore_file(file_id, output_path):
    f = fs.get(ObjectId(file_id))
    with open(output_path, "wb") as out:
        out.write(f.read())
    print(f"Datei wiederhergestellt: {output_path}")


action = input("(s)peichern oder (w)iederherstellen? ").strip().lower()

if action == "s":
    path = input("Dateipfad: ").strip()
    save_file(path)
elif action == "w":
    fid = input("File-ID: ").strip()
    out = input("Ausgabedatei: ").strip()
    restore_file(fid, out)
else:
    print("Ungültige Eingabe.")
