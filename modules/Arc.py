from modules.Coordinate import Coordinate

import math


class Arc:
    def __init__(
        self,
        direction,
        centerLat,
        centerLon,
        startLat,
        startLon,
        stopLat,
        stopLon,
        distance,
        bearing,
        angle,
    ):
        self.direction = direction
        self.cCenter = Coordinate(centerLat, centerLon)
        self.cStart = Coordinate(startLat, startLon)
        self.cStop = Coordinate(stopLat, stopLon)
        self.distance = distance
        self.bearing = bearing
        self.angle = angle
        self.coordinates = []
        self.draw()

    def draw(self):
        endBearing = self.cCenter.haversineGreatCircleBearing(
            self.cStop.lat, self.cStop.lon
        )
        start = self.bearing if self.bearing else 0
        stop = endBearing if self.cStop.lat else 360
        bearing = start
        bearingLoLimit = start
        bearingHiLimit = stop + 360 if start > stop else stop
        if self.direction == "L":
            bearing = stop
            bearingLoLimit = stop
            bearingHiLimit = start + 360 if start < stop else start
        if self.cStart.lat:
            self.coordinates.append(self.cStart)
        resultArray = []
        while bearing >= bearingLoLimit and bearing <= bearingHiLimit:
            modBearing = math.fmod(bearing + 360.0, 360.0)
            resultPoint = Coordinate()
            resultPoint.fromPBD(
                self.cCenter.lat, self.cCenter.lon, modBearing, self.distance
            )
            resultArray.append(resultPoint)
            bearing += self.angle
        if self.direction == "L":
            # Reverse the array
            resultArray = resultArray[::-1]
        for res in resultArray:
            self.coordinates.append(res)
        if self.cStop.lat:
            self.coordinates.append(self.cStop)
