from modules.CIFPAirport import CIFPAirport
from modules.CIFPFix import CIFPFix
from modules.CIFPRestrictive import CIFPRestrictive
from modules.CIFPVOR import CIFPVOR
from modules.FileHandler import FileHandler

# CIFP Data
NAVDATA_DIR = "./navdata"
CIFP_FILENAME = "FAACIFP18"
CIFP_PATH = f"{NAVDATA_DIR}/{CIFP_FILENAME}"
# CIFP Line Definitions
CIFP_AIRPORT_PREFIX = "SUSAP"
CIFP_NAVAID_PREFIX = "SUSAD"
CIFP_FIX_PREFIX = "SUSAE"
CIFP_RESTRICTIVE_PREFIX = "SUSAU"


class CIFP:
    def __init__(
        self,
        airportIds: list = [],
        fixIds: list = [],
        vorIds: list = [],
        restrictiveIds: list = [],
    ):
        self.exists = False
        self.airportsToParse = airportIds
        self.airportLines = []
        self.fixesToParse = fixIds
        self.fixLines = []
        self.vorsToParse = vorIds
        self.vorLines = []
        self.restrictiveToParse = restrictiveIds
        self.restrictiveLines = []
        self.setUpPath()
        self.parseCIFP()

    def setUpPath(self):
        fh = FileHandler()
        if fh.checkFile(CIFP_PATH):
            self.exists = True
        else:
            print(
                f"Unable to find CIFP file at {CIFP_PATH}. Please ensure it is downloaded and in the {NAVDATA_DIR} directory."
            )

    def parseCIFP(self):
        if self.exists:
            with open(CIFP_PATH) as cifpFile:
                cifpData = cifpFile.readlines()
                for line in cifpData:
                    self.processLine(line)

    def processLine(self, line: str):
        if line.startswith(CIFP_AIRPORT_PREFIX):
            self.airportLines.append(line)
        if line.startswith(CIFP_FIX_PREFIX):
            self.fixLines.append(line)
        if line.startswith(CIFP_NAVAID_PREFIX):
            self.vorLines.append(line)
        if line.startswith(CIFP_RESTRICTIVE_PREFIX):
            self.restrictiveLines.append(line)

    def processAirportLines(self):
        cifpAirports = []
        for airport in self.airportsToParse:
            airportLines = []
            airportLine = f"{CIFP_AIRPORT_PREFIX} {airport.ljust(4,' ')}"
            for line in self.airportLines:
                if line.startswith(airportLine):
                    airportLines.append(line)
            cifpAirport = CIFPAirport(airport, airportLines)
            cifpAirports.append(cifpAirport.toDict())
        return cifpAirports

    def processFixLines(self):
        cifpFixes = []
        for fix in self.fixesToParse:
            fixLine = f"{CIFP_FIX_PREFIX}AENRT   {fix}"
            for line in self.fixLines:
                if line.startswith(fixLine):
                    cifpFix = CIFPFix(fix, line)
                    cifpFixes.append(cifpFix.toDict())
        return cifpFixes

    def processVORLines(self):
        cifpVors = []
        for vor in self.vorsToParse:
            vorLine = f"{CIFP_NAVAID_PREFIX}        {vor}"
            for line in self.vorLines:
                if line.startswith(vorLine):
                    cifpVor = CIFPVOR(vor, line)
                    cifpVors.append(cifpVor.toDict())
        return cifpVors

    def processRestrictiveLines(self):
        cifpRestrictive = []
        for restrictive in self.restrictiveToParse:
            restLines = []
            for line in self.restrictiveLines:
                if line[8:19].strip() == restrictive:
                    restLines.append(line)
            cifpRest = CIFPRestrictive(restrictive, restLines)
            cifpRestrictive.append(cifpRest.toDict())
        return cifpRestrictive
