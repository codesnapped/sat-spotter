import json

from rich.console import Console

from sat_spotter.config import CONFIG_PATH


def run_list():
    console = Console()
    data = json.loads(CONFIG_PATH.read_text())

    if not data:
        console.print("No tracked satellites.")
        return
    
    for i, sat in enumerate(data):
        console.print(f"{i + 1}. {sat['name']} ({sat['norad_id']})")