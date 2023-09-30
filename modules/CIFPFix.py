from modules.CIFPFunctions import CIFPFunctions


class CIFPFix:
    def __init__(self, id, cifpLine):
        self.id = id
        self.lat = None
        self.lon = None
        self.magvar = None
        self.cifpLine = cifpLine
        self.setFix()

    def setFix(self):
        cf = CIFPFunctions()
        coord = cf.convertDMS(self.cifpLine[32:51])
        self.lat = coord.lat
        self.lon = coord.lon
        self.magvar = cf.convertMagVar(self.cifpLine[74:79])

    def toDict(self):
        del self.cifpLine
        return self.__dict__
