from modules.CIFPFunctions import CIFPFunctions


class CIFPVOR:
    def __init__(self, id: str, cifpLine: str):
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

    def toDict(self):
        del self.cifpLine
        return self.__dict__
