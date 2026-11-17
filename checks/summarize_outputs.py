"""Summarize the QGIS output (outputs/address_check.gpkg) into the numbers shown on the map.
Usage (from the repository root): python3 checks/summarize_outputs.py
Writes outputs/summary_by_hall.csv."""
import csv, sqlite3

con = sqlite3.connect("outputs/address_check.gpkg")
q = lambda sql: con.execute(sql).fetchone()[0]
n = q("SELECT COUNT(*) FROM address_check")
far_assigned = q("SELECT COUNT(*) FROM address_check WHERE AsgDist > 5")
far_nearest = q("SELECT COUNT(*) FROM address_check WHERE HubDist > 5")
mismatch = q("SELECT COUNT(*) FROM address_check WHERE mismatch = 1")
mismatch_small = q("SELECT COUNT(*) FROM address_check WHERE mismatch = 1 AND AsgDist - HubDist < 0.5")
far_hall1 = q("SELECT COUNT(*) FROM address_check WHERE AsgDist > 5 AND station = 'PRINCE GEORGE HALL 1'")
no_zone = q("SELECT COUNT(*) FROM address_check WHERE station IS NULL")

print(f"Address points:                          {n:,}")
print(f"Outside every response zone:             {no_zone}")
print(f"> 5 km from assigned hall (straight):    {far_assigned:,} ({far_assigned/n:.1%})")
print(f"  ...of which in the Hall 1 zone:        {far_hall1:,} ({far_hall1/far_assigned:.0%})")
print(f"> 5 km from nearest hall (straight):     {far_nearest:,} ({far_nearest/n:.1%})")
print(f"Nearest hall differs from assigned hall: {mismatch:,} ({mismatch/n:.1%}); "
      f"{mismatch_small:,} of them ({mismatch_small/mismatch:.0%}) differ by < 0.5 km")

rows = con.execute("""SELECT station, COUNT(*), ROUND(AVG(AsgDist), 2), ROUND(MAX(AsgDist), 2),
                             SUM(AsgDist > 5), SUM(mismatch = 1)
                      FROM address_check GROUP BY station ORDER BY station""").fetchall()
with open("outputs/summary_by_hall.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["assigned_hall", "address_points", "mean_km", "max_km", "over_5km", "nearest_differs"])
    w.writerows(rows)
print("\nBy assigned hall (written to outputs/summary_by_hall.csv):")
for r in rows:
    print("  ", r)
