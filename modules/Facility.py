from modules.FileHandler import FileHandler

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
