from modules.FileHandler import FileHandler

import json

BOUNDARY_DIR = "./boundaries"


class Boundary:
    def __init__(self, id):
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
