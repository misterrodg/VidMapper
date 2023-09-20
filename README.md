# VidMapper

A simple Python-based VidMap draw tool for use with [vNAS](https://virtualnas.net).

it is designed to be a stopgap for any facilities that do not have available vidmap data, or low traffic facilities that might not merit a FOIA request.

## Testing Note

If you would like to test your maps prior to loading them into [vNAS Data Admin](https://data-admin.virtualnas.net/login), [GeoJSON.io](https://geojson.io) is a great tool.

## Requirements

Python3.8 or Later (Tested with Python 3.10.12)

# Instructions for Use

First, download the FAA CIFP zip file. Copy the `FAACIFP18` file from the zip into the `./navdata` directory.

Next, create a facility file. This file will define what should be drawn into the map.

## Facility File Format

An example facility file is available in the root folder as `example_fac.json`.

The facility json file must contain the following sections, whether or not they contain data:

- `id`: The FAA three letter identifier for the facility
- `magvar`: The magnetic variance for the facility.
- `airports`: An array of airport objects.
- `fixes`: An array of fix objects. These print as crossed lines at the fix location.
- `rnav_points`: An array of RNAV point names. These print as the RNAV point symbol (four-pointed star).
- `vors`: An array of VOR objects.
- `restrictive`: An array of restrictive (Alert, Caution, Danger, MOA, Prohibited, Restricted, Training, Warning) airspace names.

### Airport Objects

The airport object must contain the following sections, whether or not they contain data:

- `id`: The identifier for the airport. For airports with an ICAO code, use the ICAO code. Otherwise, use the FAA code (generally only necessary for smaller airports).
- `runways`: A boolean value that tells the script to print the runways for the airport.
- `symbol`: A boolean value that tells the script to print an airport symbol for the airport.
- `centerlines`: An array of centerline objects.

#### Centerline Objects

The centerline object must contain the following sections, whether or not they contain data:

- `runway`: The identifier for the runway in the format `RW[0][0][L/C/R]`. Example: `RW04L`.
- `length`: An integer length value that the centerlines should extend to.
- `fixes`: An array of fix names that tells the script to print a crossbar at the fix location.

### Fix Objects

The fix object must contain the following sections, whether or not they contain data:

- `id`: The identifier for the fix.
- `defined_by`: An array of VORs that define the fix.

### VOR Objects

The VOR object must contain the following sections, whether or not they contain data:

- `id`: The identifier for the VOR.
- `innerOnly`: A boolean value that tells the script to print only the inner circle for the VOR. Useful for VORs at airports.

## Drawing the Facility

Run the following command, where `AAA` is the FAA three letter identifier for the facility:

```
python3 draw.py --facility=[AAA]
```
