from modules.Circle import Circle
from modules.Cross import Cross
from modules.FileHandler import FileHandler
from modules.FRD import FRD
from modules.RNAV import RNAV

import json

FIX_DIR = "./navdata/fixes"


class Fix:
    def __init__(self, magvar, fixObject):
        self.id = None
        self.magvar = magvar
        self.definedBy = None
        self.rnavPoint = None
        self.frdPoint = None
        self.lat = None
        self.lon = None
        self.filePath = ""
        # Drawn Data
        self.featureArray = []
        self.verifyFixObject(fixObject)
        self.getFixData()

    def verifyFixObject(self, fixObject):
        if fixObject:
            if "id" in fixObject:
                self.id = fixObject["id"]
                self.filePath = f"{FIX_DIR}/{self.id}.json"
            if "defined_by" in fixObject:
                self.definedBy = fixObject["defined_by"]
            if "rnav_point" in fixObject:
                self.rnavPoint = fixObject["rnav_point"]
            if "frd_point" in fixObject:
                self.frdPoint = fixObject["frd_point"]

    def getFixData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                fixData = json.load(jsonFile)
                if "lat" in fixData:
                    if type(fixData["lat"]) == float:
                        self.lat = fixData["lat"]
                if "lon" in fixData:
                    if type(fixData["lon"]) == float:
                        self.lon = fixData["lon"]

    def drawFix(self):
        if (self.lat != None and self.lon != None) or (self.frdPoint != None):
            if self.rnavPoint == True:
                SIDES = 24
                RADIUS = 0.3
                rnavPoint = RNAV(self.lat, self.lon, SIDES, RADIUS, self.magvar)
                for feature in rnavPoint.featureArray:
                    self.featureArray.append(feature)
            else:
                if self.frdPoint:
                    LENGTH = 1
                    frd = FRD(LENGTH, self.frdPoint)
                    for feature in frd.featureArray:
                        self.featureArray.append(feature)
                else:
                    if self.definedBy:
                        LENGTH = 1
                        cross = Cross(self.lat, self.lon, LENGTH, self.definedBy)
                        for feature in cross.featureArray:
                            self.featureArray.append(feature)
                    else:
                        SIDES = 3
                        RADIUS = 0.2
                        triangle = Circle(
                            self.lat, self.lon, SIDES, RADIUS, self.magvar
                        )
                        self.featureArray.append(triangle.feature)
