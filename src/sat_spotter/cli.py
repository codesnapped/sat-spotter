"""CLI entry point for Sat-Spotter."""

import argparse

from sat_spotter.passes import run_passes
from sat_spotter.remove import run_remove
from sat_spotter.search import run_search

def main():

    parser = argparse.ArgumentParser(description="Satellite pass prediction")
    subparsers = parser.add_subparsers(dest="command")

    passes_parser = subparsers.add_parser("passes", help="Predict satellite passes")
    passes_parser.add_argument("--lat", type=float, default=52.23, help="Observer location latitude")
    passes_parser.add_argument("--lon", type=float, default=21.01, help="Observer location longitude")
    passes_parser.add_argument("--hours", type=int, default=24, help="Hours to look ahead")
    passes_parser.add_argument("--elev", type=int, default=10, help="Minimum elevation filter")
    passes_parser.add_argument("--tz", type=str, default="Europe/Warsaw", help="Timezone for time display")
    passes_parser.add_argument("--visible-only", dest="visible_only", action="store_true", help="Only show visible passes")

    search_parser = subparsers.add_parser("search", help="Search for satellites on Celestrak")
    search_parser.add_argument("name", type=str, help="Satellite name to search for")

    remove_parser = subparsers.add_parser("remove", help="Remove a satellite from tracked list")

    args = parser.parse_args()
    if args.command is None:
        args = parser.parse_args(["passes"])
    
    if args.command == "passes":
        run_passes(args)
    elif args.command == "search":
        run_search(args)
    elif args.command == "remove":
        run_remove()


if __name__ == "__main__":
    main()
