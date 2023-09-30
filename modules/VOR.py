from modules.Circle import Circle


class VOR:
    def __init__(self, magvar: int, vorDefinition: dict, vorObject: dict):
        self.id = None
        self.magvar = magvar
        self.innerOnly = False
        self.lat = 0
        self.lon = 0
        # Drawn Data
        self.featureArray = []
        self.verifyVORDefinition(vorDefinition)
        self.verifyVORObject(vorObject)

    def verifyVORDefinition(self, vorDefinition: dict):
        if "id" in vorDefinition:
            self.id = vorDefinition["id"]
        if "inner_only" in vorDefinition:
            self.innerOnly = vorDefinition["inner_only"]

    def verifyVORObject(self, vorObject: dict):
        if "id" in vorObject:
            self.id = vorObject["id"]
        if "lat" in vorObject:
            self.lat = vorObject["lat"]
        if "lon" in vorObject:
            self.lon = vorObject["lon"]

    def drawVOR(self):
        SIDES = 24
        INNER_RADIUS = 0.05
        OUTER_RADIUS = 0.45
        inner = Circle(self.lat, self.lon, SIDES, INNER_RADIUS, self.magvar)
        self.featureArray.append(inner.feature)
        if not self.innerOnly:
            outer = Circle(self.lat, self.lon, SIDES, OUTER_RADIUS, self.magvar)
            self.featureArray.append(outer.feature)
