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

The facility json file has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `id`<span style="color:#FF0000">\*</span>: The FAA three letter identifier for the facility
- `magvar`<span style="color:#FF0000">\*</span>: The magnetic variance for the facility.
- `airports`: An array of airport objects.
- `fixes`: An array of fix objects. These print as crossed lines, a triangle, or an RNAV point symbol (four-pointed star) at the fix location.
- `vors`: An array of VOR objects.
- `restrictive`: An array of restrictive (Alert, Caution, Danger, MOA, Prohibited, Restricted, Training, Warning) airspace names.

### Airport Objects

The airport object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `id`<span style="color:#FF0000">\*</span>: The identifier for the airport. For airports with an ICAO code, use the ICAO code. Otherwise, use the FAA code (generally only necessary for smaller airports).
- `runways`: A boolean value that tells the script to print the runways for the airport.
- `symbol`: A boolean value that tells the script to print an airport symbol for the airport.
- `centerlines`: An array of centerline objects.

#### Centerline Objects

The centerline object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `runway`<span style="color:#FF0000">\*</span>: The identifier for the runway in the format `RW[0][0][L/C/R]`. Example: `RW04L`.
- `length`<span style="color:#FF0000">\*</span>: An integer length value that the centerlines should extend to.
- `crossbars`: An array of decimal values that tells the script to print a crossbar at that distance from the runway threshold.

### Fix Objects

The fix object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `id`<span style="color:#FF0000">\*</span>: The identifier for the fix.
- `defined_by`: An array of VORs that define the fix.
- `rnav_point`: A boolean value that tells the script to draw this point as an RNAV point symbol (four-pointed star). This overrides any defines in `defined_by`.

**NOTE**: If `defined_by` is omitted, the fix object will be drawn as a triangle rather than crossed lines.

### VOR Objects

The VOR object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `id`<span style="color:#FF0000">\*</span>: The identifier for the VOR.
- `inner_only`: A boolean value that tells the script to print only the inner circle for the VOR. Useful for VORs at airports.

## Drawing the Facility

Run the following command, where `AAA` is the FAA three letter identifier for the facility:

```
python3 draw.py --facility=[AAA]
```
