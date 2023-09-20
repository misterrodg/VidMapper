from modules.Airport import Airport
from modules.CIFP import CIFP
from modules.FileHandler import FileHandler
from modules.VOR import VOR

import json

FACILITY_DIR = "./facilities"


class Facility:
    def __init__(self, id):
        self.id = id
        self.magvar = None
        self.airports = None
        self.fixes = None
        self.rnavPoints = None
        self.vors = None
        self.restrictive = None
        self.filePath = f"{FACILITY_DIR}/{id}.json"
        self.getFacilityData()
        self.checkAirports()
        self.checkVORs()

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
                if "rnav_points" in facilityData:
                    self.rnavPoints = facilityData["rnav_points"]
                if "vors" in facilityData:
                    self.vors = facilityData["vors"]
                if "restrictive" in facilityData:
                    self.restrictive = facilityData["restrictive"]
        else:
            print(f"Cannot find the {self.id} facility file.")
            print(
                f"Follow the README to create the {self.id} facility file in {FACILITY_DIR}"
            )

    def checkAirports(self):
        cf = CIFP()
        if self.airports:
            airportIds = []
            for airport in self.airports:
                airportIds.append(airport["id"])
            cf.checkForAirports(airportIds)

    def drawAirports(self):
        if self.airports:
            for airport in self.airports:
                airportData = Airport(airport)

    def checkVORs(self):
        cf = CIFP()
        if self.vors:
            vorIds = []
            for vor in self.vors:
                vorIds.append(vor["id"])
            cf.checkForVORs(vorIds)

    def drawVORs(self):
        if self.vors:
            for vor in self.vors:
                vorData = VOR(vor)
