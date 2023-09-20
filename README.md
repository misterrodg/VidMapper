# VidMapper

A simple Python-based VidMap draw tool for use with [vNAS](https://virtualnas.net).

it is designed to be a stopgap for any facilities that do not have available vidmap data, or low traffic facilities that might not merit a FOIA request.

## Requirements

Python3.8 or Later (Tested with Python 3.10.12)

## Instructions for Use

To draw a facility, run the following command, where `AAA` is the FAA three letter identifier for the facility:

```
python3 draw.py --facility=[AAA]
```
