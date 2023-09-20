from modules.FileHandler import FileHandler

import json

AIRPORT_DIR = "./navdata/airports"


class Airport:
    def __init__(self, magvar, airportObject):
        self.id = None
        self.magvar = magvar
        self.drawRunways = False
        self.drawCircle = True
        self.drawCricleBarbs = True
        self.lat = None
        self.lon = None
        self.runways = None
        self.filePath = f"{AIRPORT_DIR}/{id}.json"
        # Drawn Data
        self.runwayData = None
        self.circleData = None
        self.circleBarbData = None
        self.verifyAirportObject(airportObject)
        self.getAirportData()

    def verifyAirportObject(self, airportObject):
        if airportObject:
            if "id" in airportObject:
                self.id = airportObject["id"]
            if "runways" in airportObject:
                self.drawRunways = airportObject["runways"]
            if "symbol" in airportObject:
                self.drawCircle = airportObject["symbol"]
                self.drawCircleBarbs = airportObject["symbol"]

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
