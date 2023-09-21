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

    def setVOR(self):
        cf = CIFPFunctions()
        vorData = self.cifpLine[32:51]
        dmeData = self.cifpLine[55:74]
        dmsLine = vorData if vorData.strip() != "" else dmeData
        coord = cf.convertDMS(dmsLine)
        self.lat = coord.lat
        self.lon = coord.lon
        self.magvar = cf.convertMagVar(self.cifpLine[74:79])

    def toJsonFile(self, filePath):
        del self.cifpLine
        with open(filePath, "w") as jsonFile:
            json.dump(self.__dict__, jsonFile)
