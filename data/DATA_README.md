# Data used in this project

Downloaded 2026-11-17 with `get_data.py` (in this folder) from the City of Prince George ArcGIS REST services
(open data portal: https://opendata.princegeorge.ca). All GeoJSON files are in WGS 84 (EPSG:4326).

| File | Source layer | Features | Key fields |
|---|---|---|---|
| `fire_hall_response_zones.geojson` | OpenData_AdminBoundary / Fire Hall Response Zones (layer 15) | 52 polygons | `station` = PRINCE GEORGE HALL 1–4 (13 / 11 / 14 / 14 zones) |
| `civic_addresses.geojson` (not committed; run `get_data.py`) | OpenData_Address / Civic Address Labels (layer 4) | 29,873 points | `PointType` (29,872 Parcel, 1 Unit), `FullName` |
| `roads.geojson` (not committed; run `get_data.py`) | OpenData_RoadTraffic / Road (layer 4) | 5,425 lines | `OneWay` (1,340 one-way), `SpeedLimit` |
| `pg_fire_halls.csv` | Hall addresses from the City's Emergency services page (https://princegeorge.ca/node/49); coordinates from the City's civic address points for those addresses | 4 points | `hall_no`, `address`, `lat`, `lon`; OpenStreetMap positions agree within 19–51 m |

Checks done on download:
- Feature counts match the server counts; no duplicate OBJECTIDs.
- Each fire hall point falls inside a response zone of its own hall.

Notes:
- The zone metadata says the zones "are defined by the City of Prince George Fire Services department" and are maintained with fire dispatch. It does not say how they were drawn.
- Address points are one per parcel and include non-residential parcels; they are not households or population.

Licence: Contains information licensed under the Open Government License – City of Prince George
(https://pgmapinfo.princegeorge.ca/opendata/CityofPrinceGeorge_Open_Government_License_Open_Data.pdf).
