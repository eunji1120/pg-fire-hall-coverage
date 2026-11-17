"""Download the City of Prince George open data used in this project (GeoJSON, WGS84).
Source: City of Prince George ArcGIS REST services (open data portal https://opendata.princegeorge.ca).
Contains information licensed under the Open Government License - City of Prince George.
Usage: python3 get_data.py   (writes the .geojson files next to this script)"""
import json, os, subprocess, urllib.parse
BASE = "https://services2.arcgis.com/CnkB6jCzAsyli34z/ArcGIS/rest/services"
LAYERS = {
    "fire_hall_response_zones.geojson": "OpenData_AdminBoundary/FeatureServer/15",
    "civic_addresses.geojson":          "OpenData_Address/FeatureServer/4",
    "roads.geojson":                    "OpenData_RoadTraffic/FeatureServer/4",
}
here = os.path.dirname(os.path.abspath(__file__))
def get(url):
    return json.loads(subprocess.run(["curl", "-s", url], capture_output=True, text=True).stdout)
for fname, layer in LAYERS.items():
    n = get(f"{BASE}/{layer}/query?where=1%3D1&returnCountOnly=true&f=json")["count"]
    feats, off = [], 0
    while off < n:
        q = urllib.parse.urlencode({"where": "1=1", "outFields": "*", "outSR": 4326, "f": "geojson",
                                    "resultOffset": off, "resultRecordCount": 2000, "orderByFields": "OBJECTID"})
        page = get(f"{BASE}/{layer}/query?{q}")["features"]
        if not page: break
        feats += page; off += len(page)
    json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(here, fname), "w"))
    print(f"{fname}: {len(feats)} features (server count {n})")
