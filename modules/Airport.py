from modules.Centerline import Centerline
from modules.Circle import Circle
from modules.CircleBarbs import CircleBarbs
from modules.Line import Line


class Airport:
    def __init__(self, magvar: int, airportDefinition: dict, airportObject: dict):
        self.id = None
        self.magvar = magvar
        self.drawRunways = False
        self.drawCircle = True
        self.drawCricleBarbs = True
        self.centerlines = None
        self.lat = 0
        self.lon = 0
        self.runways = None
        self.pairedRunways = []
        # Drawn Data
        self.featureArray = []
        self.verifyAirportDefinition(airportDefinition)
        self.verifyAirportObject(airportObject)

    def verifyAirportDefinition(self, airportDefinition: dict):
        if "id" in airportDefinition:
            self.id = airportDefinition["id"]
        if "runways" in airportDefinition:
            self.drawRunways = airportDefinition["runways"]
        if "symbol" in airportDefinition:
            self.drawCircle = airportDefinition["symbol"]
            self.drawCircleBarbs = airportDefinition["symbol"]
        if "centerlines" in airportDefinition:
            self.centerlines = airportDefinition["centerlines"]

    def verifyAirportObject(self, airportObject: dict):
        if "lat" in airportObject:
            self.lat = airportObject["lat"]
        if "lon" in airportObject:
            self.lon = airportObject["lon"]
        if "runways" in airportObject:
            self.runways = airportObject["runways"]
        if "paired_runways" in airportObject:
            self.pairedRunways = airportObject["paired_runways"]
        if not self.runways and not self.pairedRunways:
            self.drawRunways = False
            self.drawCircle = True
            self.drawCricleBarbs = True

    def drawAirport(self):
        if self.lat and self.lon:
            SIDES = 24
            RADIUS = 0.3
            if self.drawCircle:
                circle = Circle(self.lat, self.lon, SIDES, RADIUS, self.magvar)
                self.featureArray.append(circle.feature)
            if self.drawCircleBarbs:
                BARB_NUMBER = 4
                BARB_LENGTH = 0.2
                circleBarbs = CircleBarbs(
                    self.lat, self.lon, BARB_NUMBER, BARB_LENGTH, RADIUS, self.magvar
                )
                for feature in circleBarbs.featureArray:
                    self.featureArray.append(feature)
            if self.drawRunways:
                for runway in self.pairedRunways:
                    runwayLine = Line(
                        runway["baseLat"],
                        runway["baseLon"],
                        runway["recipLat"],
                        runway["recipLon"],
                    )
                    self.featureArray.append(runwayLine.feature)
            if self.centerlines:
                for centerline in self.centerlines:
                    if "runway" in centerline:
                        cline = Centerline(
                            centerline["runway"],
                            self.pairedRunways,
                            centerline["length"],
                            centerline["crossbars"],
                        )
                        for feature in cline.featureArray:
                            self.featureArray.append(feature)
