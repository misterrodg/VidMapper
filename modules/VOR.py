from modules.Circle import Circle
from modules.FileHandler import FileHandler

import json

VOR_DIR = "./navdata/vors"


class VOR:
    def __init__(self, magvar, vorObject):
        self.id = None
        self.magvar = magvar
        self.innerOnly = False
        self.lat = None
        self.lon = None
        self.filePath = None
        # Drawn Data
        self.featureArray = []
        self.verifyVORObject(vorObject)
        self.getVORData()

    def verifyVORObject(self, vorObject):
        if vorObject:
            if "id" in vorObject:
                self.id = vorObject["id"]
                self.filePath = f"{VOR_DIR}/{self.id}.json"
            if "inner_only" in vorObject:
                self.innerOnly = vorObject["inner_only"]

    def getVORData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                vorData = json.load(jsonFile)
                if "lat" in vorData:
                    self.lat = vorData["lat"]
                if "lon" in vorData:
                    self.lon = vorData["lon"]

    def drawVOR(self):
        SIDES = 24
        INNER_RADIUS = 0.05
        OUTER_RADIUS = 0.45
        inner = Circle(self.lat, self.lon, SIDES, INNER_RADIUS, self.magvar)
        self.featureArray.append(inner.feature)
        if not self.innerOnly:
            outer = Circle(self.lat, self.lon, SIDES, OUTER_RADIUS, self.magvar)
            self.featureArray.append(outer.feature)
