from modules.Coordinate import Coordinate
from modules.Line import Line
from modules.VOR import VOR

import math


class Cross:
    def __init__(self, lat, lon, length, defines):
        self.lat = lat
        self.lon = lon
        self.length = length
        self.defines = defines
        self.featureArray = []
        self.draw()

    def draw(self):
        for point in self.defines:
            vorObject = {"id": point}
            vor = VOR(0, vorObject)
            if type(vor.lat) == float and type(vor.lon) == float:
                innerPoint = Coordinate(self.lat, self.lon)
                outerPoint = Coordinate(self.lat, self.lon)
                bearing = innerPoint.haversineGreatCircleBearing(vor.lat, vor.lon)
                innerPoint.fromPBD(self.lat, self.lon, bearing, self.length * 0.5)
                bearing = math.fmod(bearing + 180, 360)
                outerPoint.fromPBD(self.lat, self.lon, bearing, self.length * 0.5)
                line = Line(
                    innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon
                )
                self.featureArray.append(line.feature)
