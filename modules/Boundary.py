from modules.FileHandler import FileHandler

import json
import urllib.request

BOUNDARY_DIR = "./boundaries"


class Boundary:
    def __init__(self, id: str):
        self.id = id
        self.filePath = f"{BOUNDARY_DIR}/{id}.json"
        self.featureArray = []
        self.getBoundaryData()

    def getBoundaryData(self):
        fh = FileHandler()
        if fh.checkFile(self.filePath):
            with open(self.filePath) as jsonFile:
                boundaryData = json.load(jsonFile)
                boundaryData = self.toLineString(boundaryData)
                self.featureArray.append(boundaryData)
        else:
            self.downloadData()

    def toLineString(self, boundaryData):
        result = boundaryData
        if "geometry" in result:
            geometry = result["geometry"]
            if "type" in geometry:
                if geometry["type"] == "MultiPolygon":
                    geometry["type"] = "LineString"
                    if "coordinates" in geometry:
                        geometry["coordinates"] = geometry["coordinates"][0][0]
                        result["geometry"] = geometry
        return result

    def downloadData(self):
        url = f"https://raw.githubusercontent.com/vatsimnetwork/simaware-tracon-project/main/Boundaries/{self.id}/{self.id}.json"
        try:
            with urllib.request.urlopen(url) as res:
                jsonData = json.load(res)
                with open(self.filePath, "w") as jsonFile:
                    json.dump(jsonData, jsonFile)
            self.getBoundaryData()
        except:
            print(f"Unable to find boundary for {self.id}")
