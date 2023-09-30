from modules.Coordinate import Coordinate
from modules.Line import Line

import math


class Cross:
    def __init__(self, lat: float, lon: float, lineLength: float, defines: list):
        self.lat = lat
        self.lon = lon
        self.lineLength = lineLength
        self.defines = defines
        self.featureArray = []
        self.draw()

    def draw(self):
        for vor in self.defines:
            if "id" in vor and "lat" in vor and "lon" in vor:
                innerPoint = Coordinate(self.lat, self.lon)
                outerPoint = Coordinate(self.lat, self.lon)
                bearing = innerPoint.haversineGreatCircleBearing(vor["lat"], vor["lon"])
                innerPoint.fromPBD(self.lat, self.lon, bearing, self.lineLength * 0.5)
                bearing = math.fmod(bearing + 180, 360)
                outerPoint.fromPBD(self.lat, self.lon, bearing, self.lineLength * 0.5)
                line = Line(
                    innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon
                )
                self.featureArray.append(line.feature)
