from modules.Coordinate import Coordinate


class CIFPFunctions:
    def convertDMS(self, cifpDMSSubstring: str):
        latString = cifpDMSSubstring[0:9]
        lonString = cifpDMSSubstring[9:19]
        northSouth = latString[0:1]
        latD = int(latString[1:3])
        latM = int(latString[3:5])
        latS = int(latString[5:]) / 100
        eastWest = lonString[0:1]
        lonD = int(lonString[1:4])
        lonM = int(lonString[4:6])
        lonS = int(lonString[6:]) / 100
        coord = Coordinate()
        coord.fromDMS(northSouth, latD, latM, latS, eastWest, lonD, lonM, lonS)
        return coord

    def convertMagVar(self, cifpMagVarSubstring: str):
        magVarValue = int(cifpMagVarSubstring[1:]) / 10
        if cifpMagVarSubstring[0:1] == "W":
            magVarValue = -magVarValue
        return magVarValue
