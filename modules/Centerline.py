from modules.Coordinate import Coordinate
from modules.Crossbar import Crossbar
from modules.Line import Line


class Centerline:
    def __init__(
        self, runwayId: str, pairedRunways: list, length: int, crossbars: list
    ):
        self.runwayId = runwayId
        self.pairedRunways = pairedRunways
        self.length = length
        self.crossbars = crossbars
        self.featureArray = []
        self.draw()

    def findRunway(self):
        pairedRunway = {}
        position = None
        if self.pairedRunways:
            for runway in self.pairedRunways:
                pairId = runway["id"]
                pairIds = pairId.split("/")
                for count, rw in enumerate(pairIds):
                    if rw == self.runwayId:
                        pairedRunway = runway
                        position = count
        if position == 1:
            baseLat = pairedRunway["baseLat"]
            baseLon = pairedRunway["baseLon"]
            pairedRunway["baseLat"] = pairedRunway["recipLat"]
            pairedRunway["baseLon"] = pairedRunway["recipLon"]
            pairedRunway["recipLat"] = baseLat
            pairedRunway["recipLon"] = baseLon
        return pairedRunway

    def draw(self):
        BAR_LENGTH = 1
        if self.pairedRunways:
            pairedRunway = self.findRunway()
            if "baseLat" in pairedRunway:
                recip = Coordinate(pairedRunway["recipLat"], pairedRunway["recipLon"])
                base = Coordinate(pairedRunway["baseLat"], pairedRunway["baseLon"])
                bearing = recip.haversineGreatCircleBearing(base.lat, base.lon)
                fromPoint = base
                for i in range(self.length):
                    toPoint = Coordinate()
                    toPoint.fromPBD(fromPoint.lat, fromPoint.lon, bearing, BAR_LENGTH)
                    if i % 2 == 1:
                        line = Line(
                            fromPoint.lat, fromPoint.lon, toPoint.lat, toPoint.lon
                        )
                        self.featureArray.append(line.feature)
                    fromPoint = toPoint
                for bar in self.crossbars:
                    coord = Coordinate()
                    coord.fromPBD(base.lat, base.lon, bearing, bar)
                    crossbar = Crossbar(coord.lat, coord.lon, bearing, BAR_LENGTH)
                    self.featureArray.append(crossbar.feature)
