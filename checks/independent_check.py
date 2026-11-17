"""Independent re-check of the headline numbers without QGIS.
Uses great-circle (haversine) distance and a ray-casting point-in-polygon test on the raw
GeoJSON from data/ (run data/get_data.py first). Results should be close to, but not identical
with, the QGIS output, which measures in the BC Albers projection (EPSG:3005).
Usage (from the repository root): python3 checks/independent_check.py"""
import csv, json, math

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))

def in_ring(x, y, ring):
    inside, j = False, len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][:2]; xj, yj = ring[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside

halls = {int(h["hall_no"]): (float(h["lat"]), float(h["lon"])) for h in csv.DictReader(open("data/pg_fire_halls.csv"))}
zones = []
for z in json.load(open("data/fire_hall_response_zones.geojson"))["features"]:
    g = z["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    zones += [(int(z["properties"]["station"][-1]), p) for p in polys]

n = far_nearest = far_assigned = mismatch = no_zone = 0
for f in json.load(open("data/civic_addresses.geojson"))["features"]:
    lon, lat = f["geometry"]["coordinates"][:2]
    n += 1
    d = {h: haversine_km(lat, lon, *xy) for h, xy in halls.items()}
    nearest = min(d, key=d.get)
    hit = [h for h, poly in zones if in_ring(lon, lat, poly[0]) and not any(in_ring(lon, lat, r) for r in poly[1:])]
    if not hit:
        no_zone += 1
        continue
    assigned = hit[0]
    far_nearest += d[nearest] > 5
    far_assigned += d[assigned] > 5
    mismatch += nearest != assigned

print(f"Address points: {n:,}; outside every zone: {no_zone}")
print(f"> 5 km from nearest hall:  {far_nearest:,} ({far_nearest/n:.1%})")
print(f"> 5 km from assigned hall: {far_assigned:,} ({far_assigned/n:.1%})")
print(f"Nearest differs from assigned: {mismatch:,} ({mismatch/n:.1%})")
