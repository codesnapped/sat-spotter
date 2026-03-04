import csv
import json
from pathlib import Path

from sat_spotter.display import degrees_to_compass, to_local_time


def export_csv(passes, filepath, timezone):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Name", "Rise", "Set", "Duration", "Max Elev", "Rise Dir", "Set Dir", "Visible"])
        for p in passes:
            writer.writerow([
                to_local_time(p['rise'], timezone, format='%d-%m'),
                p['name'],
                to_local_time(p['rise'], timezone),
                to_local_time(p['set'], timezone),
                f"{((p['set'].tt - p['rise'].tt) * 24 * 60):.1f} min",
                f"{p['elevation']:.0f}°",
                degrees_to_compass(p['rise_azimuth']),
                degrees_to_compass(p['set_azimuth']),
                "Yes" if p['is_visible'] else "No",
                ])

def export_json(passes, filepath, timezone):
    data = []
    for p in passes:
        data.append({
            "name": p['name'],
            "rise": to_local_time(p['rise'], timezone),
            "set": to_local_time(p['set'], timezone),
            "duration": f"{((p['set'].tt - p['rise'].tt) * 24 * 60):.1f} min",
            "date": to_local_time(p['rise'], timezone, format='%d-%m'),
            "elevation": f"{p['elevation']:.0f}°",
            "rise_dir": degrees_to_compass(p['rise_azimuth']),
            "set_dir": degrees_to_compass(p['set_azimuth']),
            "visible": "Yes" if p['is_visible'] else "No",
        })
    Path(filepath).write_text(json.dumps(data, indent=2))

def export_file(passes, filename: str, timezone):
    try:
        ext = Path(filename).suffix.lower()
        if ext == ".csv":
            export_csv(passes, filename, timezone)
        elif ext == ".json":
            export_json(passes, filename, timezone)
        else:
            print("Unsupported format, skipping export.")
        print(f"Data exported to {filename}")
    except OSError as e:
        print(f"Failed to export: {e}")