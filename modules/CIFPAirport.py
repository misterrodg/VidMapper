from modules.CIFPFunctions import CIFPFunctions
from modules.Coordinate import Coordinate

CIFP_AIRPORT_LINE = "A"
CIFP_RUNWAY_LINE = "G"


class CIFPAirport:
    def __init__(self, id: str, cifpLines: list):
        self.id = id
        self.lat = None
        self.lon = None
        self.magvar = None
        self.runways = []
        self.pairedRunways = []
        self.cifpLines = cifpLines
        self.setAirport()
        self.setRunways()

    def setAirport(self):
        cf = CIFPFunctions()
        for line in self.cifpLines:
            if line[12:13] == CIFP_AIRPORT_LINE:
                coord = cf.convertDMS(line[32:51])
                self.lat = coord.lat
                self.lon = coord.lon
                self.magvar = cf.convertMagVar(line[51:56])

    def findRunway(self, runwayId: str, runways: list):
        return [runway for runway in runways if runway.get("id") == runwayId][0]

    def invertRunwayId(self, runwayId: str):
        inverseRunwayId = ""
        inverseRunwayPos = ""
        mainId = runwayId[2:4]
        pos = runwayId[4:5]
        if pos != "":
            inverseRunwayPos = pos
            if pos == "L":
                inverseRunwayPos = "R"
            if pos == "R":
                inverseRunwayPos = "L"
        inverseId = (int(mainId) + 18) % 36
        inverseRunwayId = f"RW{inverseId:02d}{inverseRunwayPos}"
        return inverseRunwayId

    def setRunways(self):
        cf = CIFPFunctions()
        for line in self.cifpLines:
            if line[12:13] == CIFP_RUNWAY_LINE:
                runwayId = line[13:18]
                displacedThreshold = int(line[71:75])
                runwayCoord = cf.convertDMS(line[32:51])
                self.runways.append(
                    {
                        "id": runwayId.strip(),
                        "disp": displacedThreshold,
                        "lat": runwayCoord.lat,
                        "lon": runwayCoord.lon,
                    }
                )
        self.pairRunways()

    def pairRunways(self):
        pairedRunways = []
        halfRunways = len(self.runways) // 2
        for runway in range(halfRunways):
            runwayId = self.runways[runway]["id"]
            runwayDisp = self.runways[runway]["disp"]
            runwayLat = self.runways[runway]["lat"]
            runwayLon = self.runways[runway]["lon"]
            inverseRunwayId = self.invertRunwayId(runwayId)
            inverseRunway = self.findRunway(inverseRunwayId, self.runways)
            pairedRunway = {
                "id": f"{runwayId.strip()}/{inverseRunwayId.strip()}",
                "baseLat": runwayLat,
                "baseLon": runwayLon,
                "recipLat": inverseRunway["lat"],
                "recipLon": inverseRunway["lon"],
            }
            if runwayDisp > 0:
                pairedRunway = self.undisplaceThreshold(pairedRunway, runwayDisp)
            pairedRunways.append(pairedRunway)
        self.pairedRunways = pairedRunways

    def undisplaceThreshold(self, pairedRunway: dict, displacement: float):
        FEET_IN_NM = 6076.12
        baseCoord = Coordinate(pairedRunway["baseLat"], pairedRunway["baseLon"])
        recipCoord = Coordinate(pairedRunway["recipLat"], pairedRunway["recipLon"])
        bearing = recipCoord.haversineGreatCircleBearing(baseCoord.lat, baseCoord.lon)
        baseCoord.fromPBD(
            baseCoord.lat, baseCoord.lon, bearing, displacement / FEET_IN_NM
        )
        pairedRunway["baseLat"] = baseCoord.lat
        pairedRunway["baseLon"] = baseCoord.lon
        return pairedRunway

    def toDict(self):
        del self.cifpLines
        self.paired_runways = self.pairedRunways
        del self.pairedRunways
        return self.__dict__
