
import json

import httpx
from rich.console import Console
from rich.json import JSON

from sat_spotter.config import CONFIG_PATH
from sat_spotter.tle import parse_tle

def fetch_search_result(name: str) -> str | None:
    search_url = f"https://celestrak.org/NORAD/elements/gp.php?NAME={name}&FORMAT=TLE"
    try:
        response = httpx.get(search_url)
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as e:
        print(f"Failed to fetch search results for {name}: {e}")
        return None

def run_search(args):
    name = args.name
    tle_response = fetch_search_result(name)

    console = Console()
    if not tle_response:
        console.print("Nothing found")
        return
    console.print(f"Search results for {name}")
    
    lines = tle_response.strip().splitlines()
    satellites: dict = {}
    for i in range(0, len(lines) - 2, 3):
        chunk = "\n".join(lines[i:i+3])
        parsed = parse_tle(chunk)
        sat_name: str = parsed["name"].strip()
        norad_id: int = int(parsed["line1"].split()[1].rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        index: str = f"{int((i / 3) + 1)}"
        console.print(f'{index}. {sat_name} (NORAD: {norad_id})')
        satellites[index]= {"name": sat_name, "norad_id": norad_id}

    choice = input("Add to satellites.json (number, or Enter to skip): ")
    if not choice:
        return
    chosen_satellite = satellites[choice]
    
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text())
    else:
        data = []

    if any(s['norad_id'] == chosen_satellite['norad_id'] for s in data):                   
        console.print("Already tracked!")                                                  
        return

    data.append(chosen_satellite)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))
    console.print(JSON.from_data(data))