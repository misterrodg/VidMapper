from modules.Facility import Facility

import argparse


def processFacility(id):
    facility = Facility(id)


def main():
    # Set up Defaults
    # Set up Argument Handling
    parser = argparse.ArgumentParser(description="VidMapper")
    parser.add_argument(
        "--facility", type=str, help="The three letter identifier for the facility."
    )
    args = parser.parse_args()
    facility = args.facility
    if facility:
        processFacility(args.facility)
    else:
        print("Please select a facility with the facility flag.")
        print("Example: --facility=AAA")


if __name__ == "__main__":
    main()
