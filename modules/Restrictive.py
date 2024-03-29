from modules.Arc import Arc
from modules.Circle import Circle

import json
import math

CIRCLE_LINE_LENGTH = 0.349030413029316  # This is desired line length at an angle corresponding to 2* at 10NM
ARC_LINE_LENGTH = 1.74515206514658  # This is desired line length at an angle corresponding to 10* at 10NM
DEGREES_IN_CIRCLE = 360

NAVDATA_DIR = "./navdata"
RESTRICTIVE_DIR = f"{NAVDATA_DIR}/restrictive"


class Restrictive:
    def __init__(self, restObject: dict):
        self.id = None
        self.filePath = ""
        self.definitionsArray = []
        # Drawn Data
        self.featureArray = []
        self.verifyRestObject(restObject)

    def verifyRestObject(self, restObject: dict):
        print(restObject)
        if "id" in restObject:
            self.id = restObject["id"]
            self.filePath = f"{RESTRICTIVE_DIR}/{self.id}.json"
        if "definitions" in restObject:
            self.definitionsArray = restObject["definitions"]

    def drawCircle(self, typeObject: dict):
        if "center" in typeObject and "distance" in typeObject:
            center = typeObject["center"]
            lat = float(center[0])
            lon = float(center[1])
            distance = typeObject["distance"]
            dist = float(distance)
            angle = math.degrees(math.tan(CIRCLE_LINE_LENGTH / dist))
            sides = int(DEGREES_IN_CIRCLE // angle)
            circle = Circle(lat, lon, sides, dist)
            self.featureArray.append(circle.feature)

    def drawArc(self, typeObject: dict):
        coordinates = []
        if (
            "direction" in typeObject
            and "from" in typeObject
            and "center" in typeObject
            and "distance" in typeObject
            and "bearing" in typeObject
            and "to" in typeObject
        ):
            direction = typeObject["direction"]
            coord = typeObject["center"]
            dist = typeObject["distance"]
            bearing = typeObject["bearing"]
            start = typeObject["from"]
            stop = typeObject["to"]
            angle = math.radians(math.tan(ARC_LINE_LENGTH / dist))
            arc = Arc(
                direction,
                coord[0],
                coord[1],
                start[0],
                start[1],
                stop[0],
                stop[1],
                dist,
                bearing,
                angle,
            )
            coordinates = arc.coordinates
        return coordinates

    def drawLine(self, typeObject: dict):
        result = None
        if "point" in typeObject:
            coord = typeObject["point"]
            # GeoJSON uses LON, LAT format
            result = [coord[1], coord[0]]
        return result

    def drawDefinition(self, definition: dict):
        coordinates = []
        for item in definition:
            if "type" in item:
                restType = item["type"]
                if restType == "circle":
                    self.drawCircle(item)
                else:
                    if restType == "arc":
                        arcCoords = self.drawArc(item)
                        if arcCoords:
                            for arcCoord in arcCoords:
                                # GeoJSON uses LON, LAT format
                                coord = [arcCoord.lon, arcCoord.lat]
                                coordinates.append(coord)
                    if restType == "linePoint":
                        coord = self.drawLine(item)
                        if coord != None:
                            coordinates.append(coord)
        if coordinates:
            coordinates.append(coordinates[0])
            featureObject = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates,
                },
                "properties": {
                    "thickness": 1,
                },
            }
            self.featureArray.append(featureObject)

    def drawRestrictive(self):
        for definitions in self.definitionsArray:
            if "definition" in definitions:
                definition = definitions["definition"]
                self.drawDefinition(definition)
        self.toJsonFile()

    def toJsonFile(self):
        with open(self.filePath, "w") as jsonFile:
            json.dump(self.featureArray, jsonFile)
