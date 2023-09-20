from modules.FileHandler import FileHandler

import json

FIX_DIR = "./navdata/fixes"


class Fix:
    def __init__(self, magvar, fixObject):
        self.id = None
        self.magvar = magvar
        self.definedBy = None
        self.lat = None
        self.lon = None
        self.filePath = f"{FIX_DIR}/{id}.json"
        # Drawn Data
        self.fixData = None
        self.verifyFixObject(fixObject)
        self.getFixData()

    def verifyFixObject(self, fixObject):
        if fixObject:
            if "id" in fixObject:
                self.id = fixObject["id"]
            if "defined_by" in fixObject:
                self.definedBy = fixObject["defined_by"]

    def getFixData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                fixData = json.load(jsonFile)
                if "lat" in fixData:
                    self.lat = fixData["lat"]
                if "lon" in fixData:
                    self.lon = fixData["lon"]
