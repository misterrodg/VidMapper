from modules.CIFPFunctions import CIFPFunctions

import json


class CIFPVOR:
    def __init__(self, id, cifpLine):
        self.id = id
        self.lat = None
        self.lon = None
        self.magvar = None
        self.cifpLine = cifpLine
        self.setVOR()
        del self.cifpLine

    def setVOR(self):
        cf = CIFPFunctions()
        coord = cf.convertDMS(self.cifpLine[32:51])
        self.lat = coord.lat
        self.lon = coord.lon
        self.magvar = cf.convertMagVar(self.cifpLine[74:79])

    def toJsonFile(self, filePath):
        with open(filePath, "w") as jsonFile:
            json.dump(self.__dict__, jsonFile)
