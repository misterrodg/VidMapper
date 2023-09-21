from modules.Coordinate import Coordinate
from modules.Line import Line

import math


class Crossbar:
    def __init__(self, lat, lon, bearing, length):
        self.lat = lat
        self.lon = lon
        self.bearing = bearing
        self.length = length
        self.feature = None
        self.draw()

    def draw(self):
        PERPENDICULAR_ANGLE = 90
        bearing = math.fmod(self.bearing + PERPENDICULAR_ANGLE, 360)
        point1 = Coordinate(self.lat, self.lon)
        point2 = Coordinate(self.lat, self.lon)
        point1.fromPBD(self.lat, self.lon, bearing, self.length * 0.5)
        bearing = math.fmod(bearing + 180, 360)
        point2.fromPBD(self.lat, self.lon, bearing, self.length * 0.5)
        line = Line(point1.lat, point1.lon, point2.lat, point2.lon)
        self.feature = line.feature
