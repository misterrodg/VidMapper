from modules.Arc import Arc
from modules.Circle import Circle
from modules.FileHandler import FileHandler
from modules.Line import Line

import json
import math

LINE_LENGTH = 1.74515206514658  # This is desired line length at an angle corresponding to 10* at 10NM
DEGREES_IN_CIRCLE = 360

RESTRICTIVE_DIR = "./navdata/restrictive"


class Restrictive:
    def __init__(self, restId):
        self.id = restId
        self.filePath = f"{RESTRICTIVE_DIR}/{self.id}.json"
        self.definitionsArray = []
        # Drawn Data
        self.featureArray = []
        self.getRestData()

    def getRestData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                restData = json.load(jsonFile)
                if "definitions" in restData:
                    self.definitionsArray = restData["definitions"]

    def drawCircle(self, typeObject):
        if "center" in typeObject and "distance" in typeObject:
            coord = typeObject["center"]
            dist = typeObject["distance"]
            angle = math.radians(math.tan(LINE_LENGTH / dist))
            sides = DEGREES_IN_CIRCLE / angle
            circle = Circle(coord.lat, coord.lon, sides, dist)
            self.featureArray.append(circle.feature)

    def drawArc(self, typeObject):
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
            angle = math.radians(math.tan(LINE_LENGTH / dist))
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

    def drawLine(self, typeObject):
        result = None
        if "point" in typeObject:
            coord = typeObject["point"]
            # GeoJSON uses LON, LAT format
            result = [coord[1], coord[0]]
        return result

    def drawDefinition(self, definition):
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
