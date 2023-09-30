from modules.Coordinate import Coordinate
from modules.Line import Line

import math


class FRD:
    def __init__(
        self,
        originLat: float,
        originLon: float,
        radial: float,
        distance: float,
        lineLength: float,
    ):
        self.lat = originLat
        self.lon = originLon
        self.radial = radial
        self.distance = distance
        self.lineLength = lineLength
        self.featureArray = []
        self.draw()

    def draw(self):
        crossPoint = Coordinate()
        crossPoint.fromPBD(self.lat, self.lon, self.radial, self.distance)
        innerPoint = Coordinate(crossPoint.lat, crossPoint.lon)
        outerPoint = Coordinate(crossPoint.lat, crossPoint.lon)
        bearing = self.radial
        innerPoint.fromPBD(
            crossPoint.lat, crossPoint.lon, bearing, self.lineLength * 0.5
        )
        bearing = math.fmod(bearing + 180, 360)
        outerPoint.fromPBD(
            crossPoint.lat, crossPoint.lon, bearing, self.lineLength * 0.5
        )
        line = Line(innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon)
        self.featureArray.append(line.feature)
        bearing = math.fmod(bearing + 90, 360)
        innerPoint.fromPBD(
            crossPoint.lat, crossPoint.lon, bearing, self.lineLength * 0.5
        )
        bearing = math.fmod(bearing + 180, 360)
        outerPoint.fromPBD(
            crossPoint.lat, crossPoint.lon, bearing, self.lineLength * 0.5
        )
        line = Line(innerPoint.lat, innerPoint.lon, outerPoint.lat, outerPoint.lon)
        self.featureArray.append(line.feature)
