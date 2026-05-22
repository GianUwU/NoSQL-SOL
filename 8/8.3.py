from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["neighborhoods"]

docs = list(col.find())

# alle Koordinaten sammeln um Bounding Box zu berechnen
all_coords = []
for doc in docs:
    geo_type = doc["geometry"]["type"]
    if geo_type == "Polygon":
        for ring in doc["geometry"]["coordinates"]:
            all_coords.extend(ring)
    elif geo_type == "MultiPolygon":
        for polygon in doc["geometry"]["coordinates"]:
            for ring in polygon:
                all_coords.extend(ring)

min_lon = min(c[0] for c in all_coords)
max_lon = max(c[0] for c in all_coords)
min_lat = min(c[1] for c in all_coords)
max_lat = max(c[1] for c in all_coords)

W, H = 900, 900


def to_pixel(lon, lat):
    x = (lon - min_lon) / (max_lon - min_lon) * (W - 40) + 20
    y = H - ((lat - min_lat) / (max_lat - min_lat) * (H - 40) + 20)
    return (x, y)


im = Image.new("RGB", (W, H), (15, 15, 30))
draw = ImageDraw.Draw(im)

for doc in docs:
    geo_type = doc["geometry"]["type"]
    rings = []
    if geo_type == "Polygon":
        rings = doc["geometry"]["coordinates"]
    elif geo_type == "MultiPolygon":
        for polygon in doc["geometry"]["coordinates"]:
            rings.extend(polygon)

    for ring in rings:
        pixels = [to_pixel(c[0], c[1]) for c in ring]
        if len(pixels) >= 3:
            draw.polygon(pixels, outline=(0, 180, 200), fill=(20, 60, 80))

im.show()
im.save("neighborhoods_all.png")
print("Gespeichert als neighborhoods_all.png")
