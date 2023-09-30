from modules.Airport import Airport
from modules.Boundary import Boundary
from modules.CIFP import CIFP
from modules.FileHandler import FileHandler
from modules.Fix import Fix
from modules.Restrictive import Restrictive
from modules.VOR import VOR

import json

FACILITY_DIR = "./facilities"
NAVDATA_DIR = "./navdata"
VIDMAP_DIR = "./vidmaps"
RESTRICTIVE_DIR = f"{NAVDATA_DIR}/restrictive"


class Facility:
    def __init__(self, id: str):
        self.id = id
        self.magvar = 0
        self.airports = []
        self.airportIds = []
        self.cifpAirports = []
        self.fixes = []
        self.fixIds = []
        self.cifpFixes = []
        self.vors = []
        self.vorIds = []
        self.cifpVORs = []
        self.restrictive = []
        self.restrictiveIds = []
        self.cifpRestrictive = []
        self.filePath = f"{FACILITY_DIR}/{id}.json"
        self.vidmapPath = f"{VIDMAP_DIR}/{id}.geojson"
        self.featureArray = []
        self.getFacilityData()
        self.getCIFPData()
        self.drawFacilityData()
        self.toJsonFile(self.vidmapPath)

    def setMagVar(self, facilityData: dict):
        if "magvar" in facilityData:
            self.magvar = facilityData["magvar"]

    def setAirports(self, facilityData: dict):
        if "airports" in facilityData:
            self.airports = facilityData["airports"]
            for airport in facilityData["airports"]:
                if "id" in airport:
                    self.airportIds.append(airport["id"])

    def setFixes(self, facilityData: dict):
        if "fixes" in facilityData:
            self.fixes = facilityData["fixes"]
            for fix in facilityData["fixes"]:
                if "id" in fix and "/" not in fix:
                    self.fixIds.append(fix["id"])
                if "defined_by" in fix:
                    for vor in fix["defined_by"]:
                        self.vorIds.append(vor)
                if "frd_point" in fix:
                    defineArray = fix["frd_point"].split("/")
                    vor = defineArray[0]
                    self.vorIds.append(vor)

    def setVORs(self, facilityData: dict):
        if "vors" in facilityData:
            self.vors = facilityData["vors"]
            for vor in facilityData["vors"]:
                if "id" in vor:
                    self.vorIds.append(vor["id"])

    def setRestrictive(self, facilityData: dict):
        fh = FileHandler()
        if "restrictive" in facilityData:
            self.restrictive = facilityData["restrictive"]
            for restrictive in facilityData["restrictive"]:
                restFilePath = f"{RESTRICTIVE_DIR}/{restrictive}.json"
                if fh.checkFile(restFilePath):
                    with open(restFilePath) as restFile:
                        restData = json.load(restFile)
                        for feature in restData:
                            self.featureArray.append(feature)
                else:
                    self.restrictiveIds.append(restrictive)

    def getFacilityData(self):
        fh = FileHandler()
        fh.checkDir(RESTRICTIVE_DIR)
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                facilityData = json.load(jsonFile)
                self.setMagVar(facilityData)
                self.setAirports(facilityData)
                self.setFixes(facilityData)
                self.setVORs(facilityData)
                self.setRestrictive(facilityData)
        else:
            print(f"Cannot find the {self.id} facility file.")
            print(
                f"Follow the README to create the {self.id} facility file in {FACILITY_DIR}"
            )

    def getCIFPData(self):
        cf = CIFP(self.airportIds, self.fixIds, self.vorIds, self.restrictiveIds)
        self.cifpAirports = cf.processAirportLines()
        self.cifpFixes = cf.processFixLines()
        self.cifpVORs = cf.processVORLines()
        self.cifpRestrictive = cf.processRestrictiveLines()

    def findAirportDefinition(self, airportId: str):
        result = None
        if self.airports:
            for airport in self.airports:
                if "id" in airport and airport["id"] == airportId:
                    result = airport
        return result

    def findVORDefinition(self, vorId: str):
        result = None
        if self.vors:
            for vor in self.vors:
                if "id" in vor and vor["id"] == vorId:
                    result = vor
        return result

    def findCIFPVOR(self, vorId: str):
        result = None
        if self.cifpVORs:
            for vor in self.cifpVORs:
                if vor["id"] == vorId:
                    result = vor
        return result

    def checkForVORsInFix(self, fix: dict):
        result = []
        vors = []
        if "defined_by" in fix:
            for vor in fix["defined_by"]:
                vors.append(vor)
        if "frd_point" in fix:
            defineArray = fix["frd_point"].split("/")
            vor = defineArray[0]
            vors.append(vor)
        for vor in vors:
            cifpVOR = self.findCIFPVOR(vor)
            result.append(cifpVOR)
        return result

    def findFixDefinition(self, fixId: str):
        result = None
        if self.fixes:
            for fix in self.fixes:
                if "id" in fix and fix["id"] == fixId:
                    result = fix
        return result

    def drawBoundaries(self):
        boundaryData = Boundary(self.id)
        if boundaryData.featureArray:
            for feature in boundaryData.featureArray:
                self.featureArray.append(feature)

    def drawAirports(self):
        if self.cifpAirports:
            for airport in self.cifpAirports:
                airportDefinition = self.findAirportDefinition(airport["id"])
                if airportDefinition != None:
                    airportData = Airport(self.magvar, airportDefinition, airport)
                    airportData.drawAirport()
                    if airportData.featureArray:
                        for feature in airportData.featureArray:
                            self.featureArray.append(feature)

    def drawFixes(self):
        if self.fixes:
            for fix in self.fixes:
                if "frd_point" in fix:
                    self.cifpFixes.append(fix)
        if self.cifpFixes:
            for fix in self.cifpFixes:
                fixDefinition = self.findFixDefinition(fix["id"])
                if fixDefinition != None:
                    fixData = Fix(self.magvar, fixDefinition, fix, vors)
                    fixData.drawFix()
                    if fixData.featureArray:
                        for feature in fixData.featureArray:
                            self.featureArray.append(feature)

    def drawVORs(self):
        if self.cifpVORs:
            for vor in self.cifpVORs:
                vorDefinition = self.findVORDefinition(vor["id"])
                if vorDefinition != None:
                    vorData = VOR(self.magvar, vorDefinition, vor)
                    vorData.drawVOR()
                    if vorData.featureArray:
                        for feature in vorData.featureArray:
                            self.featureArray.append(feature)

    def drawRestrictive(self):
        if self.cifpRestrictive:
            for rest in self.cifpRestrictive:
                restData = Restrictive(rest)
                restData.drawRestrictive()
                if restData.featureArray:
                    for feature in restData.featureArray:
                        self.featureArray.append(feature)

    def drawFacilityData(self):
        self.drawBoundaries()
        self.drawAirports()
        self.drawVORs()
        self.drawFixes()
        self.drawRestrictive()

    def toJsonFile(self, filePath: str):
        jsonData = {"type": "FeatureCollection", "features": self.featureArray}
        with open(filePath, "w") as jsonFile:
            json.dump(jsonData, jsonFile)
