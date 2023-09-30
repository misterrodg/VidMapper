from modules.Facility import Facility
from modules.FileHandler import FileHandler

import argparse


def purgeNavData():
    fh = FileHandler()
    dirs = ["restrictive"]
    for dir in dirs:
        path = f"./navdata/{dir}"
        if fh.checkPath(path):
            fh.deleteAllInSubdir(".json", path)


def processFacility(id: str):
    facility = Facility(id)


def main():
    # Set up Defaults
    # Set up Argument Handling
    parser = argparse.ArgumentParser(description="VidMapper")
    parser.add_argument(
        "--facility", type=str, help="The three letter identifier for the facility."
    )
    parser.add_argument("--purge", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    purge = args.purge
    facility = args.facility
    if purge:
        purgeNavData()
    if facility:
        processFacility(args.facility)
    if not purge and not facility:
        print("Please select a facility with the facility flag.")
        print("Example: --facility=AAA")


if __name__ == "__main__":
    main()
