from modules.CIFPFunctions import CIFPFunctions

CIRCLE = "C"
CLOCKWISE_ARC = "R"
COUNTER_CLOCKWISE_ARC = "L"
GREAT_CIRCLE_LINE = "G"
RHUMB_LINE = "H"


class CIFPRestrictive:
    def __init__(self, id, cifpLines):
        self.id = id
        self.definitions = []
        self.cifpLines = cifpLines
        self.sectionedLines = []
        self.removeTextOnly()
        self.splitIntoSectionArrays()
        self.setRestrictive()

    def removeTextOnly(self):
        result = []
        for line in self.cifpLines:
            continuationRecordNo = int(line[24:25])
            # Continuation Record Numbers above 1 are supplemental textual information
            if continuationRecordNo < 2:
                result.append(line)
        self.cifpLines = result

    def splitIntoSectionArrays(self):
        result = []
        sections = []
        lastMultCode = ""
        for line in self.cifpLines:
            multipleCode = line[19:20]
            if multipleCode == "" or multipleCode != lastMultCode:
                sections.append(multipleCode)
            lastMultCode = multipleCode
        for section in sections:
            sectionArray = []
            for line in self.cifpLines:
                multipleCode = line[19:20]
                if multipleCode == section:
                    sectionArray.append(line)
            result.append(sectionArray)
        self.sectionedLines = result

    def setRestrictive(self):
        cf = CIFPFunctions()
        for section in self.sectionedLines:
            sectionDefinition = []
            nextLines = section[1:] + section[:1]
            for count, line in enumerate(section):
                nextLine = nextLines[count]
                boundaryVia = line[30:31]
                if boundaryVia == COUNTER_CLOCKWISE_ARC or boundaryVia == CLOCKWISE_ARC:
                    nextDMS = (
                        nextLine[32:51]
                        if nextLine[32:51].strip() != ""
                        else nextLine[51:70]
                    )
                    start = cf.convertDMS(line[32:51])
                    center = cf.convertDMS(line[51:70])
                    dist = int(line[70:74].strip()) / 10
                    bearing = int(line[74:78].strip()) / 10
                    stop = cf.convertDMS(nextDMS)
                    definitionObject = {
                        "type": "arc",
                        "direction": boundaryVia,
                        "from": [start.lat, start.lon],
                        "center": [center.lat, center.lon],
                        "distance": dist,
                        "bearing": bearing,
                        "to": [stop.lat, stop.lon],
                    }
                    sectionDefinition.append(definitionObject)
                if boundaryVia == CIRCLE:
                    coord = cf.convertDMS(line[51:70])
                    dist = int(line[70:74].strip()) / 10
                    definitionObject = {
                        "type": "circle",
                        "center": [coord.lat, coord.lon],
                        "distance": dist,
                    }
                    sectionDefinition.append(definitionObject)
                if boundaryVia == GREAT_CIRCLE_LINE or boundaryVia == RHUMB_LINE:
                    nextDMS = (
                        nextLine[32:51]
                        if nextLine[32:51].strip() != ""
                        else nextLine[51:70]
                    )
                    start = cf.convertDMS(line[32:51])
                    stop = cf.convertDMS(nextDMS)
                    definitionObject = {
                        "type": "linePoint",
                        "point": [start.lat, start.lon],
                    }
                    sectionDefinition.append(definitionObject)
            sectionObject = {"definition": sectionDefinition}
            self.definitions.append(sectionObject)

    def toDict(self):
        del self.cifpLines
        del self.sectionedLines
        return self.__dict__
