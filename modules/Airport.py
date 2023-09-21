from modules.Centerline import Centerline
from modules.Circle import Circle
from modules.CircleBarbs import CircleBarbs
from modules.FileHandler import FileHandler
from modules.Line import Line

import json

AIRPORT_DIR = "./navdata/airports"


class Airport:
    def __init__(self, magvar, airportObject):
        self.id = None
        self.magvar = magvar
        self.drawRunways = False
        self.drawCircle = True
        self.drawCricleBarbs = True
        self.centerlines = None
        self.lat = None
        self.lon = None
        self.runways = None
        self.pairedRunways = []
        self.filePath = ""
        # Drawn Data
        self.featureArray = []
        self.verifyAirportObject(airportObject)
        self.getAirportData()

    def verifyAirportObject(self, airportObject):
        if airportObject:
            if "id" in airportObject:
                self.id = airportObject["id"]
                self.filePath = f"{AIRPORT_DIR}/{self.id}.json"
            if "runways" in airportObject:
                self.drawRunways = airportObject["runways"]
            if "symbol" in airportObject:
                self.drawCircle = airportObject["symbol"]
                self.drawCircleBarbs = airportObject["symbol"]
            if "centerlines" in airportObject:
                self.centerlines = airportObject["centerlines"]

    def getAirportData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                airportData = json.load(jsonFile)
                if "lat" in airportData:
                    self.lat = airportData["lat"]
                if "lon" in airportData:
                    self.lon = airportData["lon"]
                if "runways" in airportData:
                    self.runways = airportData["runways"]
                if "paired_runways" in airportData:
                    self.pairedRunways = airportData["paired_runways"]

    def drawAirport(self):
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
