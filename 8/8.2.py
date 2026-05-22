from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient("mongodb://localhost:27017/")
col = client["restaurants"]["neighborhoods"]

doc = col.find_one()
coords = doc["geometry"]["coordinates"][0]  # äusserer Ring

lons = [c[0] for c in coords]
lats = [c[1] for c in coords]

min_lon, max_lon = min(lons), max(lons)
min_lat, max_lat = min(lats), max(lats)

W, H = 600, 600


def to_pixel(lon, lat):
    x = (lon - min_lon) / (max_lon - min_lon) * (W - 40) + 20
    y = H - ((lat - min_lat) / (max_lat - min_lat) * (H - 40) + 20)
    return (x, y)


pixels = [to_pixel(c[0], c[1]) for c in coords]

im = Image.new("RGB", (W, H), (20, 20, 40))
draw = ImageDraw.Draw(im)
draw.polygon(pixels, outline=(0, 200, 200), fill=(30, 80, 100))

im.show()
