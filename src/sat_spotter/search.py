
import httpx
from rich.console import Console
from rich.table import Table

from sat_spotter.tle import parse_tle

def run_search(args):
    name = args.name
    search_url = f"https://celestrak.org/NORAD/elements/gp.php?NAME={name}&FORMAT=TLE"
    tle_response: str | None

    try:
        response = httpx.get(search_url)
        response.raise_for_status()
        tle_response = response.text
    except httpx.HTTPError as e:
        print(f"Failed to fetch search results for {name}: {e}")
        return None
    
    console = Console()
    console.print(f"Search results for {name}")
    
    lines = tle_response.strip().splitlines()
    for i in range(0, len(lines) - 2, 3):
        chunk = "\n".join(lines[i:i+3])
        parsed = parse_tle(chunk)
        console.print(f'{int((i / 3) + 1)}. {parsed["name"].strip()} (NORAD: {parsed["line1"].split()[1].rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})')
