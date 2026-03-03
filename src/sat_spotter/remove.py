import json

from rich.console import Console

from sat_spotter.config import CONFIG_PATH


def run_remove():
    console = Console()
    data = json.loads(CONFIG_PATH.read_text())

    if not data:
        console.print("Nothing to remove.")
        return
    
    for i, sat in enumerate(data):
        console.print(f"{i + 1}. {sat['name']} ({sat['norad_id']})")

    choice = input("Remove from satellites.json (number, or Enter to skip): ")
    if not choice:
        return
    else:
        sat_index = int(choice) - 1
        if not (0 <= sat_index < len(data)):
            console.print("Invalid index. Skipping.")
            return
        del data[sat_index]
        CONFIG_PATH.write_text(json.dumps(data, indent=2))
        console.print("Entry deleted.")