from modules.Converter import Converter
from modules.Coordinate import Coordinate
from modules.Line import Line
from modules.VOR import VOR

import math


class FRD:
    def __init__(self, length, define):
        self.length = length
        self.define = define
        self.featureArray = []
        self.draw()

    def draw(self):
        conv = Converter()
        defineArray = self.define.split("/")
        vorId = defineArray[0]
        radial = conv.tryFloatParse(defineArray[1])
        distance = conv.tryFloatParse(defineArray[2])
        if (
            type(vorId) == str
            and (type(radial) == int or type(radial) == float)
            and (type(distance) == int or type(distance) == float)
        ):
            vorObject = {"id": defineArray[0]}
            vor = VOR(0, vorObject)
            if type(vor.lat) == float and type(vor.lon) == float:
                crossPoint = Coordinate()
                crossPoint.fromPBD(vor.lat, vor.lon, radial, distance)
                innerPoint = Coordinate(crossPoint.lat, crossPoint.lon)
                outerPoint = Coordinate(crossPoint.lat, crossPoint.lon)
                bearing = radial
                innerPoint.fromPBD(
                    crossPoint.lat, crossPoint.lon, bearing, self.length * 0.5
                )
                bearing = math.fmod(bearing + 180, 360)
                outerPoint.fromPBD(
                    crossPoint.lat, crossPoint.lon, bearing, self.length * 0.5
                )
                line = Line(
                    innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon
                )
                self.featureArray.append(line.feature)
                bearing = math.fmod(bearing + 90, 360)
                innerPoint.fromPBD(
                    crossPoint.lat, crossPoint.lon, bearing, self.length * 0.5
                )
                bearing = math.fmod(bearing + 180, 360)
                outerPoint.fromPBD(
                    crossPoint.lat, crossPoint.lon, bearing, self.length * 0.5
                )
                line = Line(
                    innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon
                )
                self.featureArray.append(line.feature)
