# VidMapper

A simple Python-based VidMap draw tool for use with [vNAS](https://virtualnas.net).

it is designed to be a stopgap for any facilities that do not have available vidmap data, or low traffic facilities that might not merit a FOIA request.

## Testing Note

If you would like to test your maps prior to loading them into [vNAS Data Admin](https://data-admin.virtualnas.net/login), [GeoJSON.io](https://geojson.io) is a great tool.

## Requirements

Python3.8 or Later (Tested with Python 3.10.12)

# Instructions for Use

First, download the FAA CIFP zip file. Copy the `FAACIFP18` file from the zip into the `./navdata` directory.

Next, create a facility file in the `./facilities` directory with the name of the facility you will be creating. For example, if you are creating a facility for Dover RAPCON, the facility file would be `DOV.json`. If the facility ID matches the ID from the [Simaware TRACON Project](https://github.com/vatsimnetwork/simaware-tracon-project/tree/main/Boundaries), it will automatically add it to your videomap. The facility file defines what should be drawn into the map.

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
- `frd_point`: A string in the format `"VOR/Radial/Distance"` (`"AML/135/12"`). This overrides `defined_by` but is overridden by `rnav_point`
- `rnav_point`: A boolean value that tells the script to draw this point as an RNAV point symbol (four-pointed star). This overrides any defines in `defined_by` or `frd_point`.

**NOTE**: If `defined_by` is omitted, the fix object will be drawn as a triangle rather than crossed lines.

### VOR Objects

The VOR object has the following properties, with the properties marked <span style="color:#FF0000">\*</span> being required:

- `id`<span style="color:#FF0000">\*</span>: The identifier for the VOR.
- `inner_only`: A boolean value that tells the script to print only the inner circle for the VOR. Useful for VORs at airports.

### Restrictive Objects

The Restrictive object is an array of restrictive airspace names.

- Alert: use the standard format of `A0[0000][A]` (A, followed by at least one number, and an optional letter, no dashes)
- [The FAA doesn't appear to use Caution airspace]
- [The FAA doesn't appear to use Danger airspace]
- MOA: use `M[MOA Name]` (see note, below)
- Prohibited, use the standard format of `P0[0000][A]` (P, followed by at least one number, and an optional letter, with no dashes)
- Restricted, use the standard format of `R0[0000][A]` (R, followed by at least one number, and an optional letter, with no dashes)
- [The FAA doesn't appear to use Training airspace]
- Warning, use the standard format of `W0[0000][A]` (W, followed by at least one number, and an optional letter, with no dashes)

**NOTE**: Naming in the CIFP file is mostly standardized, but has some quirks, particularly for MOAs. It may be worth opening the CIFP file and searching for the entry. For example, Stumpy Point MOA appears in the file as STUMPY PT. If your program supports regex, you can search with `SUSAUR..M` and start typing the MOA name right after the `M`. For longer names, the name may actually be truncated. The Tombstone MOA, for example, is truncated as `TOMBSTON A`, `TOMBSTON B` amd `TOMBSTON C`.

## Drawing the Facility

Run the following command, where `AAA` is the FAA three letter identifier for the facility:

```
python3 draw.py --facility=[AAA]
```

The resulting file will be in `./facilities/vidmaps`
