from modules.Circle import Circle
from modules.Converter import Converter
from modules.Cross import Cross
from modules.FRD import FRD
from modules.RNAV import RNAV


class Fix:
    def __init__(
        self, magvar: int, fixDefinition: dict, fixObject: dict, cifpVors: list = []
    ):
        self.id = None
        self.magvar = magvar
        self.definedBy = []
        self.rnavPoint = False
        self.frdPoint = ""
        self.cifpVors = cifpVors
        self.lat = 0
        self.lon = 0
        # Drawn Data
        self.featureArray = []
        self.verifyFixDefinition(fixDefinition)
        self.verifyFixObject(fixObject)

    def verifyFixDefinition(self, fixDefinition: dict):
        if "id" in fixDefinition:
            self.id = fixDefinition["id"]
        if "defined_by" in fixDefinition:
            self.definedBy = fixDefinition["defined_by"]
        if "rnav_point" in fixDefinition:
            self.rnavPoint = fixDefinition["rnav_point"]
        if "frd_point" in fixDefinition:
            self.frdPoint = fixDefinition["frd_point"]

    def verifyFixObject(self, fixObject: dict):
        if "id" in fixObject:
            self.id = fixObject["id"]
        if "lat" in fixObject:
            self.lat = fixObject["lat"]
        if "lon" in fixObject:
            self.lon = fixObject["lon"]

    def drawBasic(self):
        SIDES = 3
        RADIUS = 0.2
        triangle = Circle(self.lat, self.lon, SIDES, RADIUS, self.magvar)
        self.featureArray.append(triangle.feature)

    def drawRNAV(self):
        SIDES = 24
        RADIUS = 0.3
        rnavPoint = RNAV(self.lat, self.lon, SIDES, RADIUS, self.magvar)
        for feature in rnavPoint.featureArray:
            self.featureArray.append(feature)

    def drawFRD(self):
        conv = Converter()
        defineArray = self.frdPoint.split("/")
        vorId = defineArray[0]
        radial = conv.tryFloatParse(defineArray[1])
        distance = conv.tryFloatParse(defineArray[2])
        for vor in self.cifpVors:
            if (
                "id" in vor
                and "lat" in vor
                and "lon" in vor
                and vor["id"] == vorId
                and type(radial) == float
                and type(distance) == float
            ):
                LENGTH = 1
                frd = FRD(vor["lat"], vor["lon"], radial, distance, LENGTH)
                for feature in frd.featureArray:
                    self.featureArray.append(feature)

    def drawDefinedBy(self):
        LENGTH = 1
        cross = Cross(self.lat, self.lon, LENGTH, self.cifpVors)
        for feature in cross.featureArray:
            self.featureArray.append(feature)

    def drawFix(self):
        if (self.lat != None and self.lon != None) or (self.frdPoint != None):
            if self.rnavPoint == True:
                self.drawRNAV()
            else:
                if self.frdPoint:
                    self.drawFRD()
                else:
                    if self.definedBy:
                        self.drawDefinedBy()
                    else:
                        self.drawBasic()
