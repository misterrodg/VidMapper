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
        self.filePath = f"{VOR_DIR}/{id}.json"
        # Drawn Data
        self.innerData = None
        self.outerData = None
        self.verifyVORObject(vorObject)
        self.getVORData()

    def verifyVORObject(self, vorObject):
        if vorObject:
            if "id" in vorObject:
                self.id = vorObject["id"]
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
