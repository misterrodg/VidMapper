from modules.Airport import Airport
from modules.Boundary import Boundary
from modules.CIFP import CIFP
from modules.FileHandler import FileHandler
from modules.Fix import Fix
from modules.VOR import VOR

import json

FACILITY_DIR = "./facilities"
VIDMAP_DIR = f"{FACILITY_DIR}/vidmaps"


class Facility:
    def __init__(self, id):
        self.id = id
        self.magvar = None
        self.airports = []
        self.fixes = []
        self.vors = []
        self.definedBy = []
        self.restrictive = []
        self.filePath = f"{FACILITY_DIR}/{id}.json"
        self.vidmapPath = f"{VIDMAP_DIR}/{id}.json"
        self.featureArray = []
        self.getFacilityData()
        self.checkBoundaries()
        self.checkAirports()
        self.checkVORs()
        self.checkFixes()
        self.toJsonFile(self.vidmapPath)

    def getFacilityData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                facilityData = json.load(jsonFile)
                if "magvar" in facilityData:
                    self.magvar = facilityData["magvar"]
                if "airports" in facilityData:
                    self.airports = facilityData["airports"]
                if "fixes" in facilityData:
                    self.fixes = facilityData["fixes"]
                    for fix in facilityData["fixes"]:
                        if "defined_by" in fix:
                            for vor in fix["defined_by"]:
                                vorObject = {"id": vor}
                                self.definedBy.append(vorObject)
                if "vors" in facilityData:
                    self.vors = facilityData["vors"]
                if "restrictive" in facilityData:
                    self.restrictive = facilityData["restrictive"]
        else:
            print(f"Cannot find the {self.id} facility file.")
            print(
                f"Follow the README to create the {self.id} facility file in {FACILITY_DIR}"
            )

    def checkBoundaries(self):
        self.drawBoundaries()

    def drawBoundaries(self):
        boundaryData = Boundary(self.id)
        if boundaryData.featureArray:
            for feature in boundaryData.featureArray:
                self.featureArray.append(feature)

    def checkAirports(self):
        cf = CIFP()
        if self.airports:
            airportIds = []
            for airport in self.airports:
                airportIds.append(airport["id"])
            cf.checkForAirports(airportIds)
            self.drawAirports()

    def drawAirports(self):
        if self.airports:
            for airport in self.airports:
                airportData = Airport(self.magvar, airport)
                airportData.drawAirport()
                if airportData.featureArray:
                    for feature in airportData.featureArray:
                        self.featureArray.append(feature)

    def checkFixes(self):
        cf = CIFP()
        if self.fixes:
            fixIds = []
            for fix in self.fixes:
                fixIds.append(fix["id"])
            cf.checkForFixes(fixIds)
            self.drawFixes()

    def drawFixes(self):
        if self.fixes:
            for fix in self.fixes:
                fixData = Fix(self.magvar, fix)
                fixData.drawFix()
                if fixData.featureArray:
                    for feature in fixData.featureArray:
                        self.featureArray.append(feature)

    def checkVORs(self):
        cf = CIFP()
        if self.vors:
            vorIds = []
            for vor in self.vors:
                vorIds.append(vor["id"])
            for vor in self.definedBy:
                vorIds.append(vor["id"])
            cf.checkForVORs(vorIds)
            self.drawVORs()

    def drawVORs(self):
        if self.vors:
            for vor in self.vors:
                vorData = VOR(self.magvar, vor)
                vorData.drawVOR()
                if vorData.featureArray:
                    for feature in vorData.featureArray:
                        self.featureArray.append(feature)

    def toJsonFile(self, filePath):
        fh = FileHandler()
        fh.checkDir(VIDMAP_DIR)
        jsonData = {"type": "FeatureCollection", "features": self.featureArray}
        with open(filePath, "w") as jsonFile:
            json.dump(jsonData, jsonFile)
